import logging
import simpy
from .base import BaseBuffer
from src.polygon.models.buffer import BulkBufferConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BulkBuffer(BaseBuffer):
    """Буфер для сыпучих ресурсов (количеств)"""
    def __init__(
            self,
            env: simpy.Environment,
            config: BulkBufferConfig
    ) -> None:
        # Конфигурация буфера
        self.config = config
        super().__init__(env, self.config.capacity, self.config.name)

        # Инициализация буфера
        self._bulk = simpy.Container(self.env, self._capacity, self.config.initial_level)

    @staticmethod
    def _error(operation: str, reason: str, value: float) -> ValueError:
        """
        Фабрика ошибки ValueError для операций буфера

        :param operation: тип операции ("PUT" или "GET")
        :param reason: краткое описание причины ошибки
        :param value: значение, вызвавшее ошибку
        :return: экземпляр ValueError (не выбрасывается автоматически)
        """
        error_msg = f"{operation}: {reason} ({value})"
        logger.error(error_msg)
        return ValueError(error_msg)

    def put(self, quantity: float) -> simpy.Event:
        """
        Поместить партию ресурса в буфер

        :param quantity: количество ресурса для добавления
        :return: событие Simpy Event для yield
        :raises ValueError: если quantity < 0 или quantity > capacity
        """
        if quantity < 0:
            raise self._error("PUT", "отрицательное количество", quantity)

        if quantity > self._capacity:
            raise self._error("PUT", "превышает вместимость", quantity)

        logger.debug(f"[{self.name}] PUT {quantity} -> level: {self.level}/{self._capacity}, {self.env.now}")
        return self._bulk.put(quantity)

    def get(self, quantity: float) -> simpy.Event:
        """
        Извлечь партию ресурса из буфера

        :param quantity: количество ресурса для извлечения
        :return: событие Simpy Event для yield
        :raises ValueError: если quantity < 0 или quantity > capacity
        """
        if quantity < 0:
            raise self._error("GET", "отрицательное количество", quantity)

        if quantity > self._capacity:
            raise self._error("GET", "превышает вместимость", quantity)

        logger.debug(f"[{self.name}] GET {quantity} <- level: {self.level}/{self._capacity}, {self.env.now}")
        return self._bulk.get(quantity)

    @property
    def level(self) -> float:
        """Текущий уровень заполнения буфера"""
        return self._bulk.level
