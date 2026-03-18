from typing import Literal, Dict
from uuid import UUID
from collections import Counter
from pydantic import BaseModel, Field, field_validator
from .base import BasePartConfig


class AssemblyComponent(BaseModel):
    """
    Компонент сборки. Определяет шаблон компонента сборки и
    требуемое количество для сборки.
    """
    part_type_id: UUID = Field(
        ...,
        description="ID - идентификатор детали сборки (шаблона)."
    )
    quantity: int = Field(
        ...,
        ge=1,
        description="Количество деталей для сборки"
    )


class AssemblyPartConfig(BasePartConfig):
    """
    Конфигурация сборочной единицы.

    Предназначенный для деталей собираемый из нескольких компонентов:
        - узлы и агрегаты
        - комплект готового изделия
    """
    part_type: Literal["assembly"] = Field(
        default="assembly",
        description="Тип детали: сборочная единица."
    )
    specification: Dict[str, AssemblyComponent] = Field(
        ...,
        min_length=2,
        description="Спецификация сборочной единицы: {роль_компонента: конфигурация}. Минимум 2 компонента"
    )

    @field_validator("specification")
    @classmethod
    def validate_unique_component_names(cls, v: Dict[str, AssemblyComponent]) -> Dict[str, AssemblyComponent]:
        """
        Валидация уникальности имени компонента в спецификации.
        """
        names = list(v.keys())
        counter = Counter(names)

        duplicates = [name for name, count in counter.items() if count > 1]
        if duplicates:
            raise ValueError(
                f"Имена компонентов в спецификации должны быть уникальными. Обнаружены дубликаты: {duplicates}"
            )

        return v
