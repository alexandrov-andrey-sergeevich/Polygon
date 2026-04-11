from typing import Literal, Self
from pydantic import Field, model_validator
from .base import BaseCombiningConfig


class MixingProcessConfig(BaseCombiningConfig):
    object_type: Literal["mixing"] = Field(
        default="mixing",
        description="Тип процесса: смешивание"
    )

    specification: dict[str, float] = Field(
        ...,
        description="Спецификация процесса смешивания {название_ресурса: количество}"
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
