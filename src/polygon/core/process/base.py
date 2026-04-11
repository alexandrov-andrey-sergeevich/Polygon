from abc import ABC, abstractmethod
from typing import TypeVar, Generic

import simpy

from src.polygon.models.process import BaseProcessConfig
from src.polygon.core.context import SimulationContext

TConfig = TypeVar('TConfig', bound=BaseProcessConfig)


class BaseProcess(ABC, Generic[TConfig]):
    """Абстрактный базовый класс процесса"""

    def __init__(self, config: TConfig, context: SimulationContext) -> None:
        self.config = config
        self.context = context
        self.env = context.env

        # Ресурс процесса (ограничение параллельных выполнений)
        self._resource = simpy.Resource(self.env, capacity=config.capacity)
        self._running = True

        # Регистрируем процесс в контексте
        context.register_component(config.id, self)

    def run(self) -> simpy.Process:
        """
        Точка входа, запускает основной цикл процесса.
        """
        self._running = True
        return self.working()

    @abstractmethod
    def working(self) -> simpy.Process:
        """
        Основной цикл процесса (должен быть реализован в наследнике).
        """
        ...

    def stop(self) -> None:
        """Остановка процесса."""
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running
