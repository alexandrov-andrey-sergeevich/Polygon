from pydantic import Field
from ..base import BaseConfig


class BaseProcessConfig(BaseConfig):
    timeout: float = Field(
        default=0.0,
        ge=0,
        description="Время выполнения процесса"
    )

    capacity: int = Field(
        default=1,
        ge=1,
        description="Количество параллельных потоков процесса"
    )
