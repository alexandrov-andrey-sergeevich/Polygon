from typing import Literal
from uuid import UUID
from pydantic import Field
from .base import BaseBufferConfig


class DiscreteBufferConfig(BaseBufferConfig):
    """
    Буфер с дискретным типом объектов, измеряемых в штуках:
        - детали и компоненты
        - готовые изделия
        - упакованные товары

    Поддерживает политики для управления порядков извлечения элементов.
    """
    buffer_type: Literal["discrete"] = Field(
        default="discrete",
        description="Тип буфера: дискретные объекты."
    )
    queue_policy: UUID | None = Field(
        default=None,
        description="Политики управления порядком извлечения элементов."
    )