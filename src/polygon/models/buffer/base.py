from pydantic import Field
from ..base import BaseDataConfig


class BaseBufferConfig(BaseDataConfig):
    """
    Базовый класс конфигурации всех типов буферов.
    """
    capacity: int | float | None = Field(
        default=None,
        description="Максимальная емкость буфера"
    )
