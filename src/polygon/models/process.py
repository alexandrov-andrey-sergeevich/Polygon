import logging
import simpy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Process:
    def __init__(self, env: simpy.Environment, process_config):
        # Передаем окружение и настройки процесса
        self.env = env
        self.process_config = process_config

    def active_process(self):
        while True:
            try:
                # Имитируем время работы с объектом
                self.env.timeout(self.process_config.timeout)
            except simpy.Interrupt:
                logger.warning(f"", exc_info=True)
            except Exception as e:
                logger.error(f"{e}", exc_info=True)

    def __repr__(self):
        return f"Process(env={self.env}, process_config={self.process_config})"

    def __str__(self):
        ...