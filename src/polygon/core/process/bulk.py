from typing import Generator
import logging
import simpy
from .base import BaseProcess
from ..buffer import BulkBuffer
from ...models import BulkProcessConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BulkProcess(BaseProcess):
    """Процесс обработки сыпучих ресурсов"""

    def __init__(
            self,
            env: simpy.Environment,
            config: BulkProcessConfig,
            input_buffer: BulkBuffer,
            output_buffer: BulkBuffer,
    ) -> None:
        # Конфигурация процесса
        self.config = config
        super().__init__(env, self.config.timeout, self.config.capacity)

        self.input_buffer = input_buffer
        self.output_buffer = output_buffer
        self.batch_size = self.config.batch_size
        self.name = self.config.name

    def working(self) -> Generator[simpy.Event, None, None]:
        """
        Основной цикл процесса

        Извлекает партию ресурсов из входного буфера -> обрабатывает -> отправляет
        в выходной буфер
        """
        while self._running:
            with self._resource.request() as req:
                yield req

                yield self.input_buffer.get(self.batch_size)
                logger.debug(f"[{self.name}] Извлечено {self.batch_size} ед. ресурса, {self.env.now}")

                yield self.env.timeout(self.timeout)
                logger.debug(f"[{self.name}] Обработка завершена, {self.env.now}")

                yield self.output_buffer.put(self.batch_size)
                logger.debug(f"[{self.name}] Отгружено {self.batch_size} ед. ресурса, {self.env.now}")
