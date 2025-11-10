import logging
from typing import List, Any
from abc import ABC, abstractmethod
import simpy
from .part import Part

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Buffer(ABC):
    @abstractmethod
    def get_item(self, **kwargs):
        """Получаем объект из буфера"""
        raise NotImplementedError

    @abstractmethod
    def put_item(self, item: Any, **kwargs):
        """Кладем объект в буфер"""
        raise NotImplementedError

    @abstractmethod
    def get_buffer_level(self) -> int | float:
        """Текущее количество объектов в буфере"""
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.__class__.__name__


class BufferStore(Buffer):
    def __init__(self, env: simpy.Environment, buffer_config):
        # Передаем окружение и настройки буфера
        self.env = env
        self.buffer_config = buffer_config

        # Определяем тип буфера
        capacity = buffer_config.capacity if buffer_config.capacity is not None else simpy.core.Infinity
        self.buffer = simpy.Store(self.env, capacity)

    def get_item(self, **kwargs):
        """Получаем объект из буфера"""
        item = yield self.buffer.get()
        logger.info(f"Время: {self.env.now}, объект: {item.part_config.name} получена из "
                    f"буфера: {self.buffer_config.name}")
        return item

    def put_item(self, item: Part, **kwargs):
        """Кладем объект в буфер"""
        yield self.buffer.put(item)
        logger.info(f"Время: {self.env.now}, объект: {item.part_config.name} помещена в "
                    f"буфера: {self.buffer_config.name}")

    def get_buffer_level(self) -> int | float:
        """Текущее количество объектов в буфере"""
        return len(self.buffer.items)

    def get_items_list(self) -> List[Part]:
        """Список объектов в буфере"""
        return self.buffer.items.copy()

    def __repr__(self) -> str:
        return f"Buffer({self.env, self.buffer_config})\n"

    def __str__(self) -> str:
        return (f"id: {self.buffer_config.id}\n"
                f"name: {self.buffer_config.name}\n"
                f"capacity: {self.buffer_config.capacity}\n"
                f"metadata: {self.buffer_config.metadata}\n")


class BufferContainer(Buffer):
    def __init__(self, env: simpy.Environment, buffer_config):
        # Передаем окружение и настройки буфера
        self.env = env
        self.buffer_config = buffer_config

        # Определяем тип буфера
        capacity = buffer_config.capacity if buffer_config.capacity is not None else simpy.core.Infinity
        self.buffer = simpy.Container(self.env, self.buffer_config.init, capacity)

    def get_item(self, count: int | float = 1, **kwargs):
        """Получаем объект из буфера"""
        item = yield self.buffer.get(count)
        logger.info(f"Время: {self.env.now}, получено {item} объектов из буфера: {self.buffer_config.name}")
        return item

    def put_item(self, count: int | float = 1, **kwargs):
        """Кладем объект в буфер"""
        yield self.buffer.put(count)
        logger.info(f"Время: {self.env.now}, помещено {count} объектов в буфера: {self.buffer_config.name}")

    def get_buffer_level(self) -> int | float:
        """Текущее количество объектов в буфере"""
        return self.buffer.level

    def __repr__(self) -> str:
        return f"Buffer({self.env, self.buffer_config})\n"

    def __str__(self) -> str:
        return (f"id: {self.buffer_config.id}\n"
                f"name: {self.buffer_config.name}\n"
                f"capacity: {self.buffer_config.capacity}\n"
                f"metadata: {self.buffer_config.metadata}\n")