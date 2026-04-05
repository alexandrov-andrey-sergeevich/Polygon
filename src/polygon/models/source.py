from typing import Literal
from uuid import UUID
from pydantic import Field
from .base import BaseConfig


class BaseSourceConfig(BaseConfig):
    output_buffer: UUID = Field(
        ...,
        description="ID выходного буфера источника"
    )
    timeout: float = Field(
        ...,
        gt=0,
        description="Время между генерацией сущности"
    )
    batch_size: int | float = Field(
        ...,
        gt=0,
        description="Размер партии генерации сущностей"
    )


class BulkSourceConfig(BaseSourceConfig):
    object_type: Literal["bulk_source"] = Field(
        default="bulk_source",
        description="Тип генератора: протяженные сущности"
    )


class DiscreteSourceConfig(BaseSourceConfig):
    object_type: Literal["discrete_source"] = Field(
        default="discrete_source",
        description="Тип генератора: дискретные сущности"
    )
