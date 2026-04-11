from abc import ABC, abstractmethod
from typing import TypeVar, Generic

import simpy

from src.polygon.models.buffer import BaseBufferConfig
from src.polygon.core.context import SimulationContext

TConfig = TypeVar('TConfig', bound=BaseBufferConfig)


class BaseBuffer(ABC, Generic[TConfig]):
    """Абстрактный базовый класс буфера"""

    def __init__(self, config: TConfig, context: SimulationContext) -> None:
        self.config = config
        self.context = context
        self.env = context.env

        # Автоматическая регистрация в контексте симуляции
        context.register_component(config.id, self)

    @abstractmethod
    def put(self, *args, **kwargs) -> simpy.Event:
        """Поместить данные в буфер (сигнатура зависит от наследника)"""
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> simpy.Event:
        """Извлечь данные из буфера (сигнатура зависит от наследника)"""
        ...

    @property
    @abstractmethod
    def level(self) -> float:
        """Текущий уровень заполнения буфера"""
        ...
