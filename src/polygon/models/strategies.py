import logging
from typing import List, Any
from abc import ABC, abstractmethod
from .buffer import Buffer, BufferStore, BufferContainer
from .part import Part

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Strategies(ABC):
    @abstractmethod
    def get_buffer_items(self, buffer: Buffer, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def put_buffer_items(self, items: Any, buffer: Buffer, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return self.__class__.__name__


class StoreBatchStrategies(Strategies):
    """Стратегия для BufferStore (работы с объектами)"""

    def __init__(self, batch_size: int = 1):
        self.batch_size = batch_size

    def get_buffer_items(self, buffer: BufferStore, count: int | float = None, **kwargs):
        """Получить несколько объектов из Store"""
        if count is None:
            count = self.batch_size

        if count <= 0:
            raise ValueError("Количество должно быть больше 0")

        items = []
        for _ in range(count):
            try:
                item = yield from buffer.get_item(**kwargs)
                items.append(item)
            except Exception as e:
                logger.warning(f"Ошибка получения из буфера: {e}", exc_info=True)
                raise

        return items

    def put_buffer_items(self, items: List[Part] | Part, buffer: BufferStore, **kwargs):
        """Поместить объекты в Store"""
        if not isinstance(items, list):
            items = [items]

        for item in items:
            try:
                yield from buffer.put_item(item, **kwargs)
            except Exception as e:
                logger.warning(f"Ошибка помещения в буфер: {e}", exc_info=True)
                raise


class ContainerBatchStrategies(Strategies):
    """Стратегия для BufferContainer (работы с количествами)"""

    def __init__(self, batch_size: int = 1):
        self.batch_size = batch_size

    def get_buffer_items(self, buffer: BufferContainer, count: int | float = None, **kwargs):
        """Получить количество из Container"""
        if count is None:
            count = self.batch_size

        if count <= 0:
            raise ValueError("Количество должно быть больше 0")

        try:
            yield from buffer.get_item(count, **kwargs)
            return count  # Возвращаем полученное количество
        except Exception as e:
            logger.warning(f"Ошибка получения из буфера: {e}", exc_info=True)
            raise

    def put_buffer_items(self, buffer: BufferContainer, quantity: int | float = 1, **kwargs):
        """Поместить количество в Container"""
        if isinstance(quantity, list):
            # Если передан список, суммируем количества
            quantity = sum(quantity)

        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")

        try:
            yield from buffer.put_item(quantity, **kwargs)
        except Exception as e:
            logger.warning(f"Ошибка помещения в буфер: {e}", exc_info=True)
            raise