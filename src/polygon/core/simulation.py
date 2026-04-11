import simpy

from src.polygon.models.simulation import SimulationConfig
from src.polygon.core.context import SimulationContext
from src.polygon.core.registry import ComponentRegistry


class Simulation:
    """
    Основной класс симуляции.

    Принимает валидированную Pydantic-модель SimulationConfig,
    создаёт SimPy-окружение и управляет жизненным циклом симуляции.
    """

    def __init__(self, config: SimulationConfig) -> None:
        """
        Инициализация симуляции.

        :param config: Валидированная конфигурация симуляции.
        """
        self.config = config
        self.env = simpy.Environment()
        self.context = SimulationContext(self.env)

    def _create_buffers(self) -> None:
        """
        Создание всех буферов согласно конфигурации.

        Каждый буфер регистрирует себя в контексте симуляции.
        """
        for buffer_conf in self.config.buffers:
            ComponentRegistry.create(buffer_conf, self.context)

    def _create_processes(self) -> None:
        """
        Создание всех процессов согласно конфигурации и запуск их SimPy-генераторов.

        Каждый процесс регистрирует себя в контексте.
        """
        for process_conf in self.config.processes:
            process_component = ComponentRegistry.create(process_conf, self.context)
            self.env.process(process_component.run())

    def run(self) -> None:
        """
        Запуск симуляции.

        Создаёт буферы, затем процессы, и выполняет событийное моделирование
        до достижения заданной длительности.
        """
        self._create_buffers()
        self._create_processes()
        self.env.run(until=self.config.duration)
