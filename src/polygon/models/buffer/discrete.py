from typing import Literal
from pydantic import Field
from .base import BaseBufferConfig


class DiscreteBufferConfig(BaseBufferConfig):
    object_type: Literal["discrete_buffer"] = Field(
        default="discrete_buffer",
        description="Тип буфера: дискретный"
    )

    capacity: int = Field(
        ...,
        ge=1,
        description="Вместимость буфера"
    )
