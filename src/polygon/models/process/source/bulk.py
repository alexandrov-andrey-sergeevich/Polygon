from typing import Literal, Self
from uuid import UUID
from pydantic import Field, model_validator
from .base import BaseSourceConfig


class BulkSourceConfig(BaseSourceConfig):
    object_type: Literal["bulk_source"] = Field(
        default="bulk_source",
        description="Тип процесса: источник непрерывных сущностей"
    )

    output_buffer: UUID = Field(
        ...,
        description="Выходной буфер источника сущностей"
    )

    batch_size: float | None = Field(
        default=None,
        description="Размер партии генерируемых сущностей. "
                    "None - заполнение всей емкости входного буфера"
    )

    @model_validator(mode="after")
    def check_batch_size(self) -> Self:
        if self.batch_size is not None and self.batch_size <= 0:
            raise ValueError(
                f"Размер партии не может быть меньше нуля. "
                f"Текущее значение: {self.batch_size}"
            )
        return self