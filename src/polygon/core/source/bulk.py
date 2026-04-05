from typing import Generator
import simpy
from .base import BaseSource
from ..buffer import BulkBuffer
from ...models import BulkSourceConfig


class BulkSource(BaseSource):
    def __init__(
            self,
            env: simpy.Environment,
            config: BulkSourceConfig,
            output_buffer: BulkBuffer,
    ) -> None:
        self.config = config
        super().__init__(env, output_buffer)

        self.batch_size = self.config.batch_size
        self.timeout = self.config.timeout

    def working(self) -> Generator[simpy.Event, None, None]:
        while self._running:
            yield self.env.timeout(self.timeout)
            yield self.output_buffer.put(self.batch_size)

    @property
    def level(self) -> float:
        return self.output_buffer.level
