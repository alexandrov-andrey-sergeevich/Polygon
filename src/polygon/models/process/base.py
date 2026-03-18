from typing import Dict
from uuid import UUID
from pydantic import BaseModel, Field
from ..base import BaseDataConfig


class ProcessInputConfig(BaseModel):
    """
    Конфигурация входного буфера.

    Определяет из какого буфера будет забран ресурс для обработки.
    """
    buffer_id: UUID = Field(
        ...,
        description="ID входного буфера, из которого процесс забирает ресурс."
    )


class ProcessOutputConfig(BaseModel):
    """
    Конфигурация выходного буфера.

    Определяет в какой буфер будет помещен ресурс после обработки.
    """
    buffer_id: UUID = Field(
        ...,
        description="ID выходного буфера, в который процесс кладет ресурс."
    )


class BaseProcessConfig(BaseDataConfig):
    """
    Базовая конфигурация процесса.
    """
    capacity: int | float | None = Field(
        default=None,
        description="Количество одновременных операций (вместимость)"
    )
    timeout: int | float = Field(
        default=0,
        ge=0,
        description="Время обработки одного процесса."
    )
    inputs: Dict[str, ProcessInputConfig] = Field(
        ...,
        min_length=1,
        description="Входные буферы: {роль_входа: конфигурация}"
    )
    outputs: Dict[str, ProcessOutputConfig] = Field(
        ...,
        min_length=1,
        description="Выходные буферы: {роль_выхода: конфигурация}"
    )
