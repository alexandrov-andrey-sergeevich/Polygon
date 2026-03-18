from typing import Literal
from pydantic import Field
from .base import BasePartConfig


class BulkPartConfig(BasePartConfig):
    """
    Класс делимых деталей.

    Предназначен для материалов, измеряемых в объеме или массе:
        - жидкости (вода, масло, топливо)
        - сыпучие материалы (песок, цемент, зерно)
        - газы (воздух, азот, аргон)

    Отличается от дискретных деталей тем, что представляет непрерывную величину.
    """
    part_type: Literal["bulk"] = Field(
        default="bulk",
        description="Тип детали: делимые материалы."
    )
    quantity: float = Field(
        default=1.0,
        gt=0,
        description="Базовое количество материала (объём или масса)."
    )