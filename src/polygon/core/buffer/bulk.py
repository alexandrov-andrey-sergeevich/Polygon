import logging

import simpy

from .base import BaseBuffer
from src.polygon.models.buffer import BulkBufferConfig
from src.polygon.core.registry import ComponentRegistry
from src.polygon.core.context import SimulationContext

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@ComponentRegistry.registry("bulk_buffer")
class BulkBuffer(BaseBuffer[BulkBufferConfig]):
    """Буфер для сыпучих ресурсов (количеств)"""
    def __init__(self, config: BulkBufferConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        self._bulk = simpy.Container(
            self.env,
            config.capacity,
            config.initial_level
        )

    def put(self, quantity: float) -> simpy.Event:
        """Поместить партию ресурса в буфер"""
        logger.debug(
            f"[{self.config.name}] PUT {quantity} -> "
            f"level: {self.level}/{self.config.capacity}, {self.env.now}"
        )
        return self._bulk.put(quantity)

    def get(self, quantity: float) -> simpy.Event:
        """Извлечь партию ресурса из буфера"""
        logger.debug(
            f"[{self.config.name}] GET {quantity} <- "
            f"level: {self.level}/{self.config.capacity}, {self.env.now}"
        )
        return self._bulk.get(quantity)

    @property
    def level(self) -> float:
        return self._bulk.level