import logging

from src.polygon.core.process.base import BaseProcess
from src.polygon.models.process.simple import BulkSimpleProcessConfig
from src.polygon.core.context import SimulationContext
from src.polygon.core.registry import ComponentRegistry

logger = logging.getLogger(__name__)


@ComponentRegistry.registry("bulk_process")
class BulkProcess(BaseProcess[BulkSimpleProcessConfig]):
    """Процесс обработки сыпучих ресурсов"""

    def __init__(self, config: BulkSimpleProcessConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        # Получаем буферы по UUID из контекста
        self.input_buffer = context.get_component(config.input_buffer)
        self.output_buffer = context.get_component(config.output_buffer)

        if self.input_buffer is None or self.output_buffer is None:
            raise ValueError(f"Не найдены буферы для процесса {config.id}")

    def working(self):
        while self._running:
            with self._resource.request() as req:
                yield req

                yield self.input_buffer.get(self.config.batch_size)
                logger.debug(f"[{self.config.name}] Извлечено {self.config.batch_size} ед., {self.env.now}")

                yield self.env.timeout(self.config.timeout)
                logger.debug(f"[{self.config.name}] Обработка завершена, {self.env.now}")

                yield self.output_buffer.put(self.config.batch_size)
                logger.debug(f"[{self.config.name}] Отгружено {self.config.batch_size} ед., {self.env.now}")