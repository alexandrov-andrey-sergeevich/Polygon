from uuid import UUID
from pydantic import Field
from ..base import BaseProcessConfig


class BaseSimpleProcessConfig(BaseProcessConfig):
    input_buffer: UUID = Field(
        ...,
        description="Входной буфер"
    )

    output_buffer: UUID = Field(
        ...,
        description="Выходной буфер"
    )
