import logging

from src.polygon.core.process.base import BaseProcess
from src.polygon.models.process import BulkSinkConfig
from src.polygon.core.context import SimulationContext
from src.polygon.core.registry import ComponentRegistry

logger = logging.getLogger(__name__)


@ComponentRegistry.registry("bulk_sink")
class BulkSink(BaseProcess[BulkSinkConfig]):
    """Поглотитель непрерывного ресурса"""

    def __init__(self, config: BulkSinkConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        self.input_buffer = context.get_component(config.input_buffer)
        if self.input_buffer is None:
            raise ValueError(f"Буфер {config.input_buffer} не найден для стока {config.id}")

    def working(self):
        while self._running:
            with self._resource.request() as req:
                yield req

                if self.config.batch_size is None:
                    batch = self.input_buffer.level
                else:
                    batch = self.config.batch_size

                if batch > 0:
                    yield self.input_buffer.get(batch)
                    logger.debug(f"[{self.config.name}] Поглощено {batch} ед., {self.env.now}")

                yield self.env.timeout(self.config.timeout)