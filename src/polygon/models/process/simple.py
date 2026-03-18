from typing import Literal
from uuid import UUID
from pydantic import Field
from .base import BaseProcessConfig


class SimpleProcessConfig(BaseProcessConfig):
    """
    Конфигурация простого процесса.

    Предназначен для базовых операций без специальной логики:
        - транспортировка материала
        - базовая обработка деталей
    """
    process_type: Literal["simple"] = Field(
        default="simple",
        description="Тип процесса: базовый"
    )
