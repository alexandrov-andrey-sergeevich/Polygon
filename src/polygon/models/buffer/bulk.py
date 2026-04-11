from typing import Literal, Self
from pydantic import Field, model_validator
from .base import BaseBufferConfig


class BulkBufferConfig(BaseBufferConfig):
    object_type: Literal["bulk_buffer"] = Field(
        default="bulk_buffer",
        description="Тип буфера: непрерывный"
    )

    capacity: float = Field(
        ...,
        gt=0,
        description="Вместимость буфера"
    )

    initial_level: float = Field(
        default=0.0,
        ge=0.0,
        description="Начальный уровень заполнения буфера"
    )

    @model_validator(mode="after")
    def check_initial_level(self) -> Self:
        if self.initial_level > self.capacity:
            raise ValueError(
                f"Начальный уровень ({self.initial_level}) не может превышать "
                f"вместимость буфера ({self.capacity})"
            )
        return self
