from typing import Literal
from pydantic import Field
from .base import BasePartConfig


class DiscretePartConfig(BasePartConfig):
    """
    Класс дискретных деталей.

    Предназначен для отдельных объектов, измеряемых в штуках:
        - детали и компоненты
        - готовые изделия
        - упакованные товары

    Каждая деталь имеет уникальный идентификатор.
    """
    part_type: Literal["discrete"] = Field(
        default="discrete",
        description="Тип детали: дискретные объекты."
    )
