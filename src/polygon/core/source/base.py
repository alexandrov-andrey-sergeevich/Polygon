from abc import ABC, abstractmethod
from typing import Generator
import simpy
from ..buffer import BaseBuffer
from ...models import BaseSourceConfig


class BaseSource(ABC):
    def __init__(
            self,
            env: simpy.Environment,
            output_buffer: BaseBuffer
    ) -> None:
        self.env = env
        self.output_buffer = output_buffer
        self._running = True

    def run(self) -> Generator[simpy.Event, None, None]:
        self._running = True
        yield from self.working()

    @abstractmethod
    def working(self) -> Generator[simpy.Event, None, None]:
        ...

    def stop(self) -> None:
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def capacity(self) -> int | float:
        return self.output_buffer.capacity
