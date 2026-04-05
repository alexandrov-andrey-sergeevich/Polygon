from abc import ABC, abstractmethod
from typing import Generator
import simpy


class BaseProcess(ABC):
    def __init__(
            self,
            env: simpy.Environment,
            timeout: float = 0.0,
            capacity: int = 1
    ) -> None:
        self.env = env
        self.timeout = timeout
        self._capacity = capacity

        # Инициализация ресурса процесса
        self._resource = simpy.Resource(self.env, self._capacity)
        self._running = True

    def run(self) -> Generator[simpy.Event, None, None]:
        """
        Точка входа запускает основной цикл процесса

        Сбрасывает флаг _running = True и делегирует выполнение working().
        Может вызываться многократно для "перезапуска" процесса
        """
        self._running = True
        yield from self.working()

    @abstractmethod
    def working(self) -> Generator[simpy.Event, None, None]:
        """
        Основной цикл процесса

        Должен быть реализован в наследнике. Определяет логику обработки:
            - захват ресурса
            - обработка (timeout)
            - взаимодействие с входным(-ми)/выходным(-ми) буферами
        """
        ...

    def stop(self) -> None:
        """
        Остановка процесса

        Устанавливает флаг _running = False. Процесс завершает текущий цикл
        и остановится на следующей проверке while self._running
        """
        self._running = False

    @property
    def is_running(self) -> bool:
        """
        Проверка состояния процесса

        :return: True - если процесс активен; False, если остановлен
        """
        return self._running

    @property
    def capacity(self) -> int:
        """Емкость ресурса (кол-во параллельных процессов)"""
        return self._capacity