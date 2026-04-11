from typing import Literal
from pydantic import Field
from .base import BaseSimpleProcessConfig


class DiscreteSimpleProcessConfig(BaseSimpleProcessConfig):
    object_type: Literal["discrete_process"] = Field(
        default="discrete_process",
        description="Тип процесса: простой с дискретными объектами"
    )

    batch_size: int = Field(
        default=1,
        ge=1,
        description="Размер партии сущностей для обработки процессом"
    )
