from uuid import UUID, uuid4
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class BaseDataConfig(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="ID объекта")
    name: str = Field(..., min_length=3, max_length=50, description="Имя объекта")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Остальные данные")


class BufferConfig(BaseDataConfig):
    capacity: Optional[int | float] = Field(default=None, gt=0, description="Емкость буфера")
    init: Optional[int | float] = Field(default=0, ge=0, description="Начальный уровень заполнения (для типа Container)")


class PartConfig(BaseDataConfig):
    path: List[UUID] = Field(default_factory=list, description="Путь детали по симуляции")
