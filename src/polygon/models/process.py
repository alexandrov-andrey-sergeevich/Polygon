from typing import Literal, Dict
from uuid import UUID
from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from .base import BaseConfig


class BaseProcessConfig(BaseConfig):
    timeout: float = Field(
        default=1.0,
        ge=0,
        description="Время выполнения процесса"
    )
    capacity: int = Field(
        default=1,
        ge=1,
        description="Количество параллельных потоков процесса"
    )


class BulkProcessConfig(BaseProcessConfig):
    object_type: Literal["bulk_process"] = Field(
        default="bulk_process",
        description="Тип процесса: непрерывный процесс"
    )
    batch_size: float = Field(
        default=1.0,
        gt=0,
        description="Размер партии ресурса для процесса"
    )
    input_buffer_id: UUID = Field(
        ...,
        description="ID входного буфера"
    )
    output_buffer_id: UUID = Field(
        ...,
        description="ID выходного буфера"
    )


class DiscreteProcessConfig(BaseProcessConfig):
    object_type: Literal["discrete_process"] = Field(
        default="discrete_process",
        description="Тип процесса: дискретный процесс"
    )
    batch_size: int = Field(
        default=1,
        ge=1,
    )
    input_buffer_id: UUID = Field(
        ...,
        description="ID входного буфера"
    )
    output_buffer_id: UUID = Field(
        ...,
        description="ID выходного буфера"
    )


class MixingProcessConfig(BaseProcessConfig):
    object_type: Literal["mixing_process"] = Field(
        default="mixing_process",
        description="Тип процесса: смешивания непрерывных объектов"
    )
    specification: Dict[str, float] = Field(
        ...,
        description="Спецификация процесса смешивания {название_ресурса: количество}"
    )
    input_buffer_ids: Dict[str, UUID] = Field(
        ...,
        description="ID входных буферов {название_ингредиента: UUID_буфера}"
    )
    output_buffer_id: UUID = Field(
        ...,
        description="ID выходного буфера"
    )

    @field_validator("specification")
    @classmethod
    def check_specification(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Проверка количества ресурсов в спецификации"""
        if not v:
            raise ValueError("Спецификация не может быть пустой")

        for name, qty in v.items():
            if qty <= 0:
                raise ValueError(f"Количество {name} должно быть больше 0, получено: {qty}")
        return v

    @field_validator("input_buffer_ids")
    @classmethod
    def check_input_buffer_ids(cls, v: Dict[str, UUID], info: ValidationInfo) -> Dict[str, UUID]:
        """Проверка совпадения ключей входных буферов и спецификации"""
        specification: Dict[str, float] = info.data["specification"]

        if set(v.keys()) != set(specification.keys()):
            raise ValueError(
                f"Ключи входных буферов и спецификации должны совпадать. "
                f"Спецификация: {list(specification.keys())}, входные буферы: {list(v.keys())}"
            )
        return v
