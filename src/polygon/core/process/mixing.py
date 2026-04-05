from typing import Generator, Dict
import logging
import simpy
from .base import BaseProcess
from ..buffer import BulkBuffer
from ...models import MixingProcessConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MixingProcess(BaseProcess):
    """Процесс смешивания нескольких ресурсов"""

    def __init__(
            self,
            env: simpy.Environment,
            config: MixingProcessConfig,
            input_buffers: Dict[str, BulkBuffer],
            output_buffer: BulkBuffer
    ) -> None:
        # Конфигурация процесса
        self.config = config
        super().__init__(env, self.config.timeout, self.config.capacity)

        self.input_buffers = input_buffers
        self.output_buffer = output_buffer
        self.specification = self.config.specification
        self.name = self.config.name

        # Количество смеси за цикл
        self._output_quantity = sum(self.specification.values())

    def working(self) -> Generator[simpy.Event, None, None]:
        """
        Основной процесс смешивания

        Извлекает из входных буферов требуемые по спецификации ресурсы
        в указанном количестве -> смешивание -> выгрузка смеси в выходной буфер
        """
        while self._running:
            with self._resource.request() as req:
                yield req

                # Извлечь все ресурсы по спецификации
                for name, qty in self.specification.items():
                    buffer = self.input_buffers[name]
                    yield buffer.get(qty)
                    logger.debug(f"[{self.name}] Получено {qty} ед. {name}, {self.env.now}")

                # Смешивание
                yield self.env.timeout(self.timeout)
                logger.debug(f"[{self.name}] Смешивание завершено, {self.env.now}")

                # Загрузка приготовленной смеси
                yield self.output_buffer.put(self._output_quantity)
                logger.debug(f"[{self.name}] Выгружено {self._output_quantity} ед. смеси, {self.env.now}")
