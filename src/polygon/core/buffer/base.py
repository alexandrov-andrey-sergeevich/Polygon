from abc import ABC, abstractmethod
import simpy


class BaseBuffer(ABC):
    """Абстрактный базовый класс буфера"""
    def __init__(
            self,
            env: simpy.Environment,
            capacity: int | float,
            name: str | None = None
    ) -> None:
        self.env = env
        self._capacity = capacity
        self.name = name

    @property
    def capacity(self) -> int | float:
        """Емкость буфера"""
        return self._capacity

    @abstractmethod
    def put(self, *args, **kwargs) -> simpy.Event:
        """Поместить данные в буфер (сигнатура зависит от наследника)"""
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> simpy.Event:
        """Извлечь данные из буфера (сигнатура зависит от наследника)"""
        ...