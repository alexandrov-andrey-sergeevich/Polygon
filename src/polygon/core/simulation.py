import logging
import simpy
from uuid import uuid4

from src.polygon.models.buffer import BufferStore
from src.polygon.models.strategies import StoreBatchStrategies
from src.polygon.models.process import Process
from src.polygon.models.part import Part
from src.polygon.utils.validators import BufferConfig, ProcessConfig, PartConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SingleMachineSimulation:
    def __init__(self, env: simpy.Environment):
        self.env = env
        self.setup_simulation()

    def setup_simulation(self):
        """Настройка симуляции с одним станком"""

        # Создаем буферы
        self.input_buffer = BufferStore(
            self.env,
            BufferConfig(name="Входной буфер", capacity=None)
        )

        self.output_buffer = BufferStore(
            self.env,
            BufferConfig(name="Выходной буфер", capacity=15)
        )

        # Создаем стратегии и связываем их с буферами
        self.input_strategy = StoreBatchStrategies(batch_size=2)
        self.input_strategy.buffer = self.input_buffer  # Связываем с входным буфером

        self.output_strategy = StoreBatchStrategies(batch_size=2)
        self.output_strategy.buffer = self.output_buffer  # Связываем с выходным буфером

        # Создаем станок
        self.machine = Process(
            self.env,
            ProcessConfig(
                name="Станок",
                capacity=2,  # Может обрабатывать 2 детали одновременно
                timeout=5,  # Время обработки - 5 секунд
                input_strategies=self.input_strategy,
                output_strategies=self.output_strategy
            )
        )

        # Генератор деталей
        self.part_generator = self.env.process(self.generate_parts())

        # Мониторинг
        self.monitor = self.env.process(self.monitor_buffers())

    def generate_parts(self):
        """Генератор деталей для станка"""
        part_id = 1
        while True:
            # Создаем новую деталь
            part_config = PartConfig(
                id=uuid4(),
                name=f"Деталь_{part_id}",
                path=[],
                metadata={"weight": 1.5, "material": "steel"}
            )
            part = Part(part_config)

            # Помещаем деталь во входной буфер
            yield from self.input_buffer.put_item(part)
            logger.info(f"Время {self.env.now}: Создана и помещена в буфер {part.part_config.name}")

            # Ждем перед созданием следующей детали
            yield self.env.timeout(1)  # Новая деталь каждую секунду
            part_id += 1

    def monitor_buffers(self):
        """Мониторинг заполненности буферов"""
        while True:
            logger.info(f"Время {self.env.now}: "
                        f"Входной буфер: {self.input_buffer.get_buffer_level()}, "
                        f"Выходной буфер: {self.output_buffer.get_buffer_level()}/15")
            yield self.env.timeout(5)  # Логируем каждые 5 секунд

    def run_simulation(self, simulation_time=50):
        """Запуск симуляции"""
        # Запускаем станок
        self.env.process(self.run_machine())

        # Запускаем симуляцию
        logger.info("Запуск симуляции одного станка...")
        self.env.run(until=simulation_time)

        # Статистика после завершения
        self.print_statistics()

    def run_machine(self):
        """Запуск работы станка"""
        while True:
            try:
                # Используем встроенный метод процесса
                yield from self.machine.get_active_process()
            except Exception as e:
                logger.error(f"Ошибка в станке: {e}")
                yield self.env.timeout(1)  # Пауза при ошибке

    def print_statistics(self):
        """Вывод статистики после симуляции"""
        logger.info("=== СТАТИСТИКА СИМУЛЯЦИИ ===")
        logger.info(f"Деталей во входном буфере: {self.input_buffer.get_buffer_level()}")
        logger.info(f"Деталей в выходном буфере: {self.output_buffer.get_buffer_level()}")
        logger.info(
            f"Всего деталей в системе: {self.input_buffer.get_buffer_level() + self.output_buffer.get_buffer_level()}")


def main():
    env = simpy.Environment()
    simulation = SingleMachineSimulation(env)
    simulation.run_simulation(simulation_time=32)


if __name__ == "__main__":
    main()