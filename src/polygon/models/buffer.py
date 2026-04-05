from typing import Literal
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from .base import BaseConfig


class BaseBufferConfig(BaseConfig):
    capacity: int | float = Field(
        ...,
        gt=0,
        description="Вместимость буфера"
    )


class BulkBufferConfig(BaseBufferConfig):
    object_type: Literal["bulk_buffer"] = Field(
        default="bulk_buffer",
        description="Тип буфера: непрерывный"
    )
    initial_level: float = Field(
        default=0.0,
        ge=0.0,
        description="Начальный уровень заполнения буфера"
    )

    @field_validator("initial_level")
    @classmethod
    def check_initial_level(cls, v: float, info: ValidationInfo) -> float:
        capacity = info.data.get("capacity")
        if v > capacity:
            raise ValueError(f"Начальный уровень заполнения: {v}, не может превышать вместимость буфера: {capacity}")
        return v


class DiscreteBufferConfig(BaseBufferConfig):
    object_type: Literal["discrete_buffer"] = Field(
        default="discrete_buffer",
        description="Тип буфера: дискретный"
    )
    capacity: int = Field(
        ...,
        ge=1,
        description="Вместимость дискретного буфера"
    )
