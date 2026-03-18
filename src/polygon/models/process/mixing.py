from typing import Literal
from uuid import UUID
from pydantic import Field
from .base import BaseProcessConfig


class MixingProcessConfig(BaseProcessConfig):
    """
    Конфигурация процесса смешивания.

    Предназначен для создания смесей из отдельных компонентов:
        - приготовление бетонных смесей
        - создание сплавов металлов
        - смешивания химических растворов
    """
    process_type: Literal["mixing"] = Field(
        default="mixing",
        description="Тип процесса: смешивание."
    )
    mixture_part_type_id: UUID = Field(
        ...,
        description="Ссылка на шаблон смеси."
    )
