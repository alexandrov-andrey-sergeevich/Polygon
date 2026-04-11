from uuid import UUID
from pydantic import Field
from ..base import BaseProcessConfig


class BaseCombiningConfig(BaseProcessConfig):
    input_buffers: dict[str, UUID] = Field(
        ...,
        description="Входные буферы: {тип_сущности: буфер}"
    )

    output_buffer: UUID = Field(
        ...,
        description="Выходной буфер"
    )
