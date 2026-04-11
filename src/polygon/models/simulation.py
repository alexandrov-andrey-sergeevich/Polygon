from pydantic import Field
from src.polygon.models.base import BaseConfig
from src.polygon.models.process import ProcessConfig
from src.polygon.models.buffer import BufferConfig


class SimulationConfig(BaseConfig):
    duration: float = Field(
        ...,
        gt=0,
        description="Длительность симуляции"
    )

    buffers: list[BufferConfig] = Field(
        default_factory=list,
        description="Список конфигурации буферов системы"
    )

    processes: list[ProcessConfig] = Field(
        default_factory=list,
        description="Список конфигурации процессов системы"
    )
