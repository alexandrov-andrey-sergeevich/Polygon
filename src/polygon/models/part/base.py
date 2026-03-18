from typing import List
from uuid import UUID
from pydantic import Field
from ..base import BaseDataConfig


class BasePartConfig(BaseDataConfig):
    """
    Базовый класс конфигурации деталей.
    """
    description: str = Field(
        default="",
        max_length=500,
        description="Информация о детали."
    )
    route_template: List[UUID] = Field(
        ...,
        min_length=1,
        description="Последовательность узлов маршрута обработки детали."
    )
