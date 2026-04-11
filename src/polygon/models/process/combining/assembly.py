from typing import Literal, Self
from pydantic import Field, model_validator
from .base import BaseCombiningConfig


class AssemblyProcessConfig(BaseCombiningConfig):
    object_type: Literal["assembly"] = Field(
        default="assembly",
        description="Тип процесса: сборка"
    )

    specification: dict[str, int] = Field(
        ...,
        description="Спецификация процесса сборки {название_сущности: количество}"
    )

    @model_validator(mode="after")
    def check_specification(self) -> Self:
        """Проверка количества ресурсов в спецификации"""
        if not self.specification:
            raise ValueError("Спецификация не может быть пустой")

        for name, qty in self.specification.items():
            if qty <= 0:
                raise ValueError(f"Количество {name} должно быть больше 0, получено: {qty}")
        return self

    @model_validator(mode="after")
    def check_input_buffers(self) -> Self:
        """Проверка совпадения ключей входных буферов и спецификации"""
        if set(self.input_buffers.keys()) != set(self.specification.keys()):
            raise ValueError(
                f"Ключи входных буферов и спецификации должны совпадать. "
                f"Спецификация: {list(self.specification.keys())}, "
                f"входные буферы: {list(self.input_buffers.keys())}"
            )
        return self
