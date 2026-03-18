from typing import Literal
from uuid import UUID
from pydantic import Field
from .base import BaseProcessConfig


class DisassemblingProcessConfig(BaseProcessConfig):
    """
    Конфигурация процесса разборки.

    Предназначена для разделения сборочных единиц на отдельные компоненты:
        - разбор узлов на детали
        - демонтаж оборудования
    """
    process_type: Literal["disassembling"] = Field(
        default="disassembling",
        description="Тип процесса: разборка"
    )
    disassembling_part_type_id: UUID = Field(
        ...,
        description="Ссылка на шаблон разбираемой сборочной единицы."
    )