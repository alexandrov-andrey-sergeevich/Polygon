import logging
from typing import List, Any
from abc import ABC, abstractmethod
import simpy
from .buffer import Buffer, BufferStore, BufferContainer
from .part import Part

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Strategies(ABC):
    @abstractmethod
    def get_buffer_items(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def put_buffer_items(self, items: Any, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.__class__.__name__


class StoreBatchStrategies(Strategies):
    """Стратегия для BufferStore (работы с объектами)"""

    def __init__(self, batch_size: int = 1):
        self.batch_size = batch_size
        self.buffer = None  # Будет установлен извне

    def get_buffer_items(self, count: int = None, **kwargs):
        """Получить несколько объектов из Store"""
        if self.buffer is None:
            raise ValueError("Буфер не установлен для стратегии")

        if count is None:
            count = self.batch_size

        if count <= 0:
            raise ValueError("Количество должно быть больше 0")

        # Создаем процессы для каждого получения
        processes = [self.buffer.env.process(self.buffer.get_item(**kwargs)) for _ in range(int(count))]

        # Ждем завершения всех процессов
        yield simpy.AllOf(self.buffer.env, processes)

        # Получаем значения из завершенных процессов
        items = [p.value for p in processes if p.value is not None]

        logger.info(f"Время: {self.buffer.env.now}, стратегия получила {len(items)} объектов из буфера")
        return items

    def put_buffer_items(self, items: List[Part] | Part, **kwargs):
        """Поместить объекты в Store"""
        if self.buffer is None:
            raise ValueError("Буфер не установлен для стратегии")

        if not isinstance(items, list):
            items = [items]

        # Создаем процессы для каждого помещения
        processes = [self.buffer.env.process(self.buffer.put_item(item, **kwargs)) for item in items]

        # Ждем завершения всех процессов
        yield simpy.AllOf(self.buffer.env, processes)

        logger.info(f"Время: {self.buffer.env.now}, стратегия поместила {len(items)} объектов в буфер")


class ContainerBatchStrategies(Strategies):
    """Стратегия для BufferContainer (работы с количествами)"""

    def __init__(self, batch_size: int = 1):
        self.batch_size = batch_size
        self.buffer = None

    def get_buffer_items(self, count: int | float = None, **kwargs):
        """Получить количество из Container"""
        if self.buffer is None:
            raise ValueError("Буфер не установлен для стратегии")

        if count is None:
            count = self.batch_size

        if count <= 0:
            raise ValueError("Количество должно быть больше 0")

        try:
            # Создаем процесс для получения
            process = self.buffer.env.process(self.buffer.get_item(count, **kwargs))
            yield process

            actual_count = process.value if process.value is not None else 0
            logger.info(f"Время: {self.buffer.env.now}, стратегия получила {actual_count} единиц")
            return actual_count
        except Exception as e:
            logger.warning(f"Ошибка получения из буфера: {e}")
            return 0

    def put_buffer_items(self, items: Any, **kwargs):
        """Поместить количество в Container"""
        if self.buffer is None:
            raise ValueError("Буфер не установлен для стратегии")

        # Определяем количество для помещения
        if isinstance(items, list):
            quantity = len(items)
        elif isinstance(items, (int, float)):
            quantity = items
        else:
            quantity = 1

        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")

        try:
            yield from self.buffer.put_item(quantity, **kwargs)
            logger.info(f"Время: {self.buffer.env.now}, стратегия поместила {quantity} единиц")
        except Exception as e:
            logger.warning(f"Ошибка помещения в буфер: {e}")