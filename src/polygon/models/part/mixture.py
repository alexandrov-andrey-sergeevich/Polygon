from typing import Literal, Dict
from uuid import UUID
from math import isclose
from pydantic import BaseModel, Field, field_validator
from .base import BasePartConfig
from ..constants import PROPORTION_SUM_TOLERANCE, PROPORTION_MIN, PROPORTION_MAX


class MixtureComponent(BaseModel):
    """
    Класс компонента смеси.

    Определяют шаблон компонента смеси и его массовую долю в общей смеси.
    Доля должна быть в диапазоне (0.0, 1.0).
    """
    part_type_id: UUID = Field(
        ...,
        description="ID - идентификатор компонента смеси (шаблона)."
    )
    proportion: int | float = Field(
        ...,
        gt=PROPORTION_MIN,
        lt=PROPORTION_MAX,
        description="Доля компонента в смеси (0.0, 1.0)."
    )


class MixturePartConfig(BasePartConfig):
    """
    Конфигурация смеси.

    Предназначен для материалов состоящих из нескольких компонентов:
        - бетонные смеси
        - сплавы металлов
        - химические смеси
    """
    part_type: Literal["mixture"] = Field(
        default="mixture",
        description="Тип детали: смесь."
    )
    composition: Dict[str, MixtureComponent] = Field(
        ...,
        min_length=2,
        description="Состав смеси: {название_компонента: конфигурация}. Минимум 2 компонента."
    )

    @field_validator("composition")
    @classmethod
    def validate_proportion_sum(cls, v: Dict[str, MixtureComponent]) -> Dict[str, MixtureComponent]:
        """
        Валидация суммы пропорции смеси. Проверяем, что сумма всех пропорций
        равна 1.0 с заданной погрешностью.
        """
        total = sum(comp.proportion for comp in v.values())

        if not isclose(total, PROPORTION_MAX, abs_tol=PROPORTION_SUM_TOLERANCE):
            raise ValueError(
                f"Сумма пропорции смеси должна быть {PROPORTION_MAX} (+\- {PROPORTION_SUM_TOLERANCE}), "
                f"полученная: {total:.4f}. Проверьте состав: {list(v.keys())}"
            )

        return v
