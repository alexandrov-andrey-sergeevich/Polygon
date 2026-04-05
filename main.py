import logging
import simpy
from src.polygon.models import BulkBufferConfig, BulkProcessConfig, MixingProcessConfig
from src.polygon.core.buffer import BulkBuffer
from src.polygon.core.process import BulkProcess, MixingProcess

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


env = simpy.Environment()

# Входной буфер муки
flour_buffer = BulkBuffer(
    env,
    BulkBufferConfig(
        name="Буфер муки",
        capacity=50.0,
        initial_level=50.0
    )
)

# Входной буфер соли
salt_buffer = BulkBuffer(
    env,
    BulkBufferConfig(
        name="Буфер соли",
        capacity=5.0,
        initial_level=5.0
    )
)

# Выходной буфер теста
dough_buffer = BulkBuffer(
    env,
    BulkBufferConfig(
        name="Буфер теста",
        capacity=55.0,
        initial_level=0.0
    )
)

# Выходной буфер отдохнувшего теста
rest_dough_buffer= BulkBuffer(
    env,
    BulkBufferConfig(
        name="Буфер отдохнувшего теста",
        capacity=55.0,
        initial_level=0.0
    )
)

# Выходной буфер раскатанного теста
rolled_dough_buffer = BulkBuffer(
    env,
    config=BulkBufferConfig(
        name="Буфер раскатанного теста",
        capacity=55.0,
        initial_level=0.0
    )
)

# Процесс смешивания теста
mixing_dough_process = MixingProcess(
    env,
    config=MixingProcessConfig(
        name="Процесс смешивания теста",
        timeout=10.0,
        capacity=1,
        specification={
            "Мука": 50.0,
            "Соль": 5.0
        },
        input_buffer_ids={
            "Мука": flour_buffer.config.id,
            "Соль": salt_buffer.config.id
        },
        output_buffer_id=dough_buffer.config.id
    ),
    input_buffers={
            "Мука": flour_buffer,
            "Соль": salt_buffer
    },
    output_buffer=dough_buffer
)

# Процесс отдыха теста
rest_dough_process = BulkProcess(
    env,
    config=BulkProcessConfig(
        name="Отдых теста",
        timeout=15.0,
        capacity=1,
        batch_size=55.0,
        input_buffer_id=dough_buffer.config.id,
        output_buffer_id=rest_dough_buffer.config.id
    ),
    input_buffer=dough_buffer,
    output_buffer=rest_dough_buffer
)

# Процесс раскатки теста
rolling_dough_process = BulkProcess(
    env,
    config=BulkProcessConfig(
        name="Раскатка теста",
        timeout=5.0,
        capacity=1,
        batch_size=55.0,
        input_buffer_id=rest_dough_process.config.id,
        output_buffer_id=rolled_dough_buffer.config.id
    ),
    input_buffer=rest_dough_buffer,
    output_buffer=rolled_dough_buffer
)

env.process(mixing_dough_process.run())
env.process(rest_dough_process.run())
env.process(rolling_dough_process.run())

env.run(until=35)

print(rolled_dough_buffer.level)