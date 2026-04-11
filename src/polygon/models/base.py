from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="ID объекта симуляции"
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Имя объекта симуляции"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Метаданные объекта симуляции"
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
