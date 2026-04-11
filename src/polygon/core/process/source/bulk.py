import logging

from src.polygon.core.process.base import BaseProcess
from src.polygon.models.process.source.bulk import BulkSourceConfig
from src.polygon.core.context import SimulationContext
from src.polygon.core.registry import ComponentRegistry

logger = logging.getLogger(__name__)


@ComponentRegistry.registry("bulk_source")
class BulkSource(BaseProcess[BulkSourceConfig]):
    """Источник непрерывного ресурса"""

    def __init__(self, config: BulkSourceConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        self.output_buffer = context.get_component(config.output_buffer)
        if self.output_buffer is None:
            raise ValueError(f"Буфер {config.output_buffer} не найден для источника {config.id}")

    def working(self):
        while self._running:
            with self._resource.request() as req:
                yield req

                # Определяем размер генерируемой партии
                if self.config.batch_size is None:
                    # Заполняем до максимальной ёмкости
                    batch = self.output_buffer.config.capacity - self.output_buffer.level
                else:
                    batch = self.config.batch_size

                if batch > 0:
                    yield self.output_buffer.put(batch)
                    logger.debug(f"[{self.config.name}] Сгенерировано {batch} ед., {self.env.now}")

                yield self.env.timeout(self.config.timeout)