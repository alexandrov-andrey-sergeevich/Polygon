import simpy
from src.polygon.models.buffer.bulk import BulkBufferConfig


class BulkBuffer:
    def __init__(self, env: simpy.Environment, config: BulkBufferConfig):
        self.env = env
        self.config = config

        self.container = simpy.Container(
            self.env,
            capacity=self.config.capacity or simpy.core.Infinity
        )

    def add(self, quantity: float) -> simpy.Event:
        return self.container.put(quantity)

    def take(self, quantity: float) -> simpy.Event:
        return self.container.get(quantity)

    @property
    def capacity(self) -> float:
        return self.container.capacity

    @property
    def current_quantity(self) -> float:
        return self.container.level
