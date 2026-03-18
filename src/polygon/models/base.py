from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from constants import PRIORITY_MEDIUM


class BaseDataConfig(BaseModel):
    """
    Базовый класс для всех конфигураций.
    """
    id: UUID = Field(
        default_factory=uuid4,
        description="Уникальный идентификатор объекта."
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Имя объекта."
    )
    priority: int = Field(
        default=PRIORITY_MEDIUM,
        ge=0,
        description="Приоритет объекта."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Дополнительные метаданные."
    )

    model_config = ConfigDict(
        frozen=True, # Делаем конфигурацию иммутабельной
        validate_assignment=True, # Валидируем в случае изменения при frozen=False
        extra="forbid", # Запрещает не объявленные поля
    )
