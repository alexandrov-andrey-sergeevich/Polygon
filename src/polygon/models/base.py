from typing import Any, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="ID объекта симуляции"
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Имя объекта симуляции"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Метаданные объекта симуляции"
    )

    model_config = ConfigDict(
        frozen=True,  # Делаем конфигурацию иммутабельной
        extra="forbid",  # Запрещает не объявленные поля
        str_strip_whitespace=True, # Убираем лишние пробелы по краям строк
    )
