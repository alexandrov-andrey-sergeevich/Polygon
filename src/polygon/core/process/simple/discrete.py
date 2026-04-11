from typing import List, Any

import logging

from src.polygon.core.process.base import BaseProcess
from src.polygon.models.process.simple import DiscreteSimpleProcessConfig
from src.polygon.core.context import SimulationContext
from src.polygon.core.registry import ComponentRegistry

logger = logging.getLogger(__name__)


@ComponentRegistry.registry("discrete_process")
class DiscreteProcess(BaseProcess[DiscreteSimpleProcessConfig]):
    """Процесс обработки дискретных объектов"""

    def __init__(self, config: DiscreteSimpleProcessConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        self.input_buffer = context.get_component(config.input_buffer)
        self.output_buffer = context.get_component(config.output_buffer)

        if self.input_buffer is None or self.output_buffer is None:
            raise ValueError(f"Не найдены буферы для процесса {config.id}")

    def working(self):
        while self._running:
            with self._resource.request() as req:
                yield req

                items: List[Any] = []
                for _ in range(self.config.batch_size):
                    item = yield self.input_buffer.get()
                    items.append(item)
                    logger.debug(f"[{self.config.name}] Извлечен компонент: {item}")

                yield self.env.timeout(self.config.timeout)
                logger.debug(f"[{self.config.name}] Обработка компонентов завершена")

                for item in items:
                    yield self.output_buffer.put(item)
                    logger.debug(f"[{self.config.name}] Отгружен компонент: {item}")
