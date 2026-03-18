from typing import Literal
from uuid import UUID
from pydantic import Field
from .base import BaseProcessConfig


class AssemblingProcessConfig(BaseProcessConfig):
    """
    Конфигурация процесса сборки.

    Предназначен для создания сборочных единиц из отдельных деталей:
        - монтаж оборудования
        - комплектация изделия
    """
    process_type: Literal["assembling"] = Field(
        default="assembling",
        description="Тип процесса: сборка."
    )
    assembly_part_type_id: UUID = Field(
        ...,
        description="Ссылка на шаблон сборочной единицы."
    )
