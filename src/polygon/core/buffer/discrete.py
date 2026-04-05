from typing import Any, Sequence
import logging
import simpy
from .base import BaseBuffer
from src.polygon.models.buffer import DiscreteBufferConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscreteBuffer(BaseBuffer):
    """Буфер для дискретных объектов"""
    def __init__(
            self,
            env: simpy.Environment,
            config: DiscreteBufferConfig
    ) -> None:
        # Конфигурация буфера
        self.config = config
        super().__init__(env, self.config.capacity, self.config.name)

        # Инициализация буфера
        self._discrete = simpy.Store(self.env, capacity=self._capacity)

    def put(self, item: Any) -> simpy.Event:
        """
        Поместить объект в буфер

        :param item: объект добавляемый в буфер
        :return: событие SimPy Event для yield
        """
        logger.debug(f"[{self.name}] PUT {item} -> level: {len(self.items)}/{self._capacity}")
        return self._discrete.put(item)

    def get(self) -> simpy.Event:
        """
        Извлечь объект из буфера

        :return: событие SimPy Event для yield
        """
        logger.debug(f"[{self.name}] GET <- level: {len(self.items)}/{self._capacity}")
        return self._discrete.get()

    @property
    def items(self) -> Sequence[Any]:
        """Кортеж объектов в буфере"""
        return tuple(self._discrete.items)
