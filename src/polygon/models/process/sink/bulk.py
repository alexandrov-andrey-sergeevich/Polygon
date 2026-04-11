from typing import Literal, Self
from uuid import UUID
from pydantic import Field, model_validator
from .base import BaseSinkConfig


class BulkSinkConfig(BaseSinkConfig):
    object_type: Literal["bulk_sink"] = Field(
        default="bulk_sink",
        description="Тип процесса: поглотитель непрерывных сущностей"
    )
    input_buffer: UUID = Field(
        ...,
        description="Входной буфер поглотителя сущностей"
    )
    batch_size: float | None = Field(
        default=None,
        description="Размер партии поглощаемых сущностей. "
                    "None - поглощение всей емкости входного буфера"
    )

    @model_validator(mode="after")
    def check_batch_size(self) -> Self:
        if self.batch_size is not None and self.batch_size <= 0:
            raise ValueError(
                f"Размер партии не может быть меньше нуля. "
                f"Текущее значение: {self.batch_size}"
            )
        return self
