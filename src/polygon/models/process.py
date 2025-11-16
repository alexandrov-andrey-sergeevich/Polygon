import logging
import simpy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Process:
    def __init__(self, env: simpy.Environment, process_config):
        # Передаем окружение и настройки процесса
        self.env = env
        self.process_config = process_config

        # Стратегии взаимодействия с объектами
        self.input_strategies = self.process_config.input_strategies
        self.output_strategies = self.process_config.output_strategies

        # Создаем ресурс процесса
        self.resource = simpy.Resource(self.env, self.process_config.capacity)

    def get_active_process(self):
        while True:
            try:
                # Берем детали из входного буфера
                items = yield from self.input_strategies.get_buffer_items()

                # Ждем пока не освободятся места для всех деталей
                requests = [self.resource.request() for _ in range(len(items))]
                yield simpy.AllOf(self.env, requests)

                # Начинаем работу с объектами
                yield from self.active_process(items, requests)

            except simpy.Interrupt:
                logger.warning(f"Время: {self.env.now} прерывания процесса: {self.process_config.name}",
                               exc_info=True)
            except Exception as e:
                logger.error(f"Время: {self.env.now} неожиданная ошибка в процессе: {self.process_config.name}. "
                             f"Ошибка: {e}", exc_info=True)

    def active_process(self, items, requests):
        logger.info(f"Время: {self.env.now}, начало обработки в процессе {self.process_config.name}")

        # Имитируем время работы с объектом
        if self.process_config.timeout:
            yield self.env.timeout(self.process_config.timeout)  # Исправлено: добавлен yield

        logger.info(f"Время: {self.env.now}, конец обработки в процессе {self.process_config.name}")

        # Кладем детали в выходной буфер
        yield from self.output_strategies.put_buffer_items(items=items)

        # Освобождаем занятые ресурсы
        for request in requests:
            self.resource.release(request)

    def __repr__(self):
        return f"Process(env={self.env}, process_config={self.process_config})"

    def __str__(self):
        return f"Process(name={self.process_config.name}, capacity={self.process_config.capacity})"