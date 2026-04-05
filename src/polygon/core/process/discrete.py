from typing import Any, Generator, List
import logging
import simpy
from .base import BaseProcess
from ..buffer import DiscreteBuffer
from ...models import DiscreteProcessConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscreteProcess(BaseProcess):
    """Процесс обработки дискретных объектов"""

    def __init__(
            self,
            env: simpy.Environment,
            config: DiscreteProcessConfig,
            input_buffer: DiscreteBuffer,
            output_buffer: DiscreteBuffer,
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

        Извлекает партию (или единичный) объектов(-т) из входного
        буфера -> обрабатывает -> выгружает в выходной буфер
        """
        while self._running:
            with self._resource.request() as req:
                yield req

                # Список компонентов извлеченных из входного буфера
                items: List[Any] = []
                for _ in range(self.batch_size):
                    item = yield self.input_buffer.get()
                    items.append(item)
                    logger.debug(f"[{self.name}] Извлечен компонент: {item}")

                # Обрабатываем все полученные компоненты требуемое время
                yield self.env.timeout(self.timeout)
                logger.debug(f"[{self.name}] Обработка компонентов завершена")

                # Выгружаем все полученные компоненты в выходной буфер
                for item in items:
                    yield self.output_buffer.put(item)
                    logger.debug(f"[{self.name}] Отгружен компонент: {item}")
