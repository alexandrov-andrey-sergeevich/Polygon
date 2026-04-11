import logging

from src.polygon.core.process.base import BaseProcess
from src.polygon.models.process.combining import MixingProcessConfig
from src.polygon.core.context import SimulationContext
from src.polygon.core.registry import ComponentRegistry

logger = logging.getLogger(__name__)


@ComponentRegistry.registry("mixing")
class MixingProcess(BaseProcess[MixingProcessConfig]):
    """Процесс смешивания нескольких ресурсов"""

    def __init__(self, config: MixingProcessConfig, context: SimulationContext) -> None:
        super().__init__(config, context)

        # Преобразуем словарь имён буферов в словарь объектов буферов
        self.input_buffers = {
            name: context.get_component(uuid)
            for name, uuid in config.input_buffers.items()
        }
        self.output_buffer = context.get_component(config.output_buffer)

        # Проверка наличия всех буферов
        missing = [name for name, buf in self.input_buffers.items() if buf is None]
        if missing:
            raise ValueError(f"Не найдены входные буферы: {missing} для процесса {config.id}")
        if self.output_buffer is None:
            raise ValueError(f"Выходной буфер {config.output_buffer} не найден для процесса {config.id}")

        self._output_quantity = sum(config.specification.values())

    def working(self):
        while self._running:
            with self._resource.request() as req:
                yield req

                # Извлекаем ресурсы согласно спецификации
                for name, qty in self.config.specification.items():
                    buffer = self.input_buffers[name]
                    yield buffer.get(qty)
                    logger.debug(f"[{self.config.name}] Получено {qty} ед. {name}, {self.env.now}")

                # Смешивание
                yield self.env.timeout(self.config.timeout)
                logger.debug(f"[{self.config.name}] Смешивание завершено, {self.env.now}")

                # Выгрузка смеси
                yield self.output_buffer.put(self._output_quantity)
                logger.debug(f"[{self.config.name}] Выгружено {self._output_quantity} ед. смеси, {self.env.now}")