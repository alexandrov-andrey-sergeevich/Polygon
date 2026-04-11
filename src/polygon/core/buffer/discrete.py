import logging
from typing import Any, Sequence

import simpy

from .base import BaseBuffer
from src.polygon.models.buffer import DiscreteBufferConfig
from src.polygon.core.registry import ComponentRegistry
from src.polygon.core.context import SimulationContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@ComponentRegistry.registry("discrete_buffer")
class DiscreteBuffer(BaseBuffer[DiscreteBufferConfig]):
    """Буфер для дискретных объектов"""

    def __init__(self, config: DiscreteBufferConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        self._discrete = simpy.Store(self.env, config.capacity)

    def put(self, item: Any) -> simpy.Event:
        """Поместить объект в буфер"""
        logger.debug(
            f"[{self.config.name}] PUT {item} -> "
            f"level: {len(self.items)}/{self.config.capacity}"
        )
        return self._discrete.put(item)

    def get(self) -> simpy.Event:
        """Извлечь объект из буфера"""
        logger.debug(
            f"[{self.config.name}] GET <- "
            f"level: {len(self.items)}/{self.config.capacity}"
        )
        return self._discrete.get()

    @property
    def items(self) -> Sequence[Any]:
        """Кортеж объектов в буфере"""
        return tuple(self._discrete.items)

    @property
    def level(self) -> int:
        return len(self._discrete.items)
