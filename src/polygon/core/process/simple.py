from typing import Dict
import simpy
from src.polygon.models.buffer.base import BaseBufferConfig
from src.polygon.models.process.simple import SimpleProcessConfig


class SimpleProcess:
    def __init__(
            self,
            env: simpy.Environment,
            config: SimpleProcessConfig,
            input_buffer: Dict[str, BaseBufferConfig],
            output_buffer: Dict[str, BaseBufferConfig]
    ):
        self.env = env
        self.config = config
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer

        self.resource = simpy.Resource(
            self.env,
            capacity=self.config.capacity
        )

    def start(self):
        return self.env.process(self._run())

    def _run(self):
        while True:
            ...