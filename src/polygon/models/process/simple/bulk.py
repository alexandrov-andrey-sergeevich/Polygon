from typing import Literal
from pydantic import Field
from .base import BaseSimpleProcessConfig


class BulkSimpleProcessConfig(BaseSimpleProcessConfig):
    object_type: Literal["bulk_process"] = Field(
        default="bulk_process",
        description="Тип процесса: простой с непрерывными сущностями"
    )

    batch_size: float = Field(
        default=1.0,
        gt=0,
        description="Размер партии сущностей для обработки процессом"
    )
