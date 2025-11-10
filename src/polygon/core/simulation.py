# simple_simulation.py
import simpy
import logging
from src.polygon.models.buffer import BufferStore
from src.polygon.models.part import Part
from src.polygon.utils.validators import BufferConfig, PartConfig
from src.polygon.models.strategies import StoreBatchStrategies

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def simple_simulation():
    env = simpy.Environment()

    # Буферы
    buffer1 = BufferStore(env, BufferConfig(name="Накопительный", capacity=None))
    buffer2 = BufferStore(env, BufferConfig(name="Обрабатывающий", capacity=10))

    strategy = StoreBatchStrategies(batch_size=10)

    def producer():
        for i in range(25):  # Создаем 25 деталей
            part = Part(PartConfig(name=f"Деталь_{i}", path=[]))
            yield from buffer1.put_item(part)
            logger.info(
                f"Создана Деталь_{i}, в буфере 1: {buffer1.get_buffer_level()} деталей")  # FIX: добавил информацию об уровне
            yield env.timeout(0.5)  # Быстрое производство

    def transfer():
        batches = 0
        while batches < 2:  # Перенесем 2 партии
            current_level = buffer1.get_buffer_level()
            if current_level >= 10:
                logger.info(f"🔄 Начинаю перенос партии из {current_level} деталей...")
                items = yield from strategy.get_buffer_items(buffer1, count=10)
                yield from strategy.put_buffer_items(items, buffer2)
                batches += 1
                logger.info(
                    f"✅ Перенесена партия {batches}, в буфере 2: {buffer2.get_buffer_level()}/10 деталей")  # FIX: добавил информацию об уровне
            yield env.timeout(1)

    def monitor():
        while True:
            level1 = buffer1.get_buffer_level()
            level2 = buffer2.get_buffer_level()
            logger.info(f"📊 Монитор: Буфер1={level1}, Буфер2={level2}/10")
            yield env.timeout(3)

    env.process(producer())
    env.process(transfer())
    env.process(monitor())

    logger.info("🚀 Запуск симуляции...")
    env.run(until=20)


if __name__ == "__main__":
    simple_simulation()