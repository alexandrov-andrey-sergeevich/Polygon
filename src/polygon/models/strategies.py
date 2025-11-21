import logging
from typing import List, Any, Union, Dict, Optional
from abc import ABC, abstractmethod
import simpy
from .buffer import BufferStore, BufferContainer
from .part import Part
from ..utils.validators import PartConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Strategies(ABC):
    @abstractmethod
    def get_buffer_items(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def put_buffer_items(self, items: Any, **kwargs):
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class StoreBatchStrategies(Strategies):
    """Стратегия для BufferStore (работы с объектами)"""
    def __init__(self, buffer: BufferStore, batch_size: int = 1):
        self.batch_size = batch_size # Размер партии
        self.buffer = buffer # Буфер с которым взаимодействуем

    def get_buffer_items(self, count: Optional[int] = None, **kwargs):
        """Получить несколько объектов из Store"""
        if self.buffer is None:
            logger.error(f"Буфер не установлен для стратегии")
            raise ValueError("Буфер не установлен для стратегии")

        if count is None:
            logger.debug(f"Установлен стандартный объем партии")
            count = self.batch_size

        if count <= 0:
            logger.error(f"Количество должно быть больше 0")
            raise ValueError("Количество должно быть больше 0")

        logger.info(f"Время: {self.buffer.env.now}, стратегия ожидает объекты из буфера")

        # Создаем процессы для каждого получения
        processes = [self.buffer.env.process(self.buffer.get_item(**kwargs)) for _ in range(int(count))]

        # Ждем завершения всех процессов
        yield simpy.AllOf(self.buffer.env, processes)

        # Получаем значения из завершенных процессов
        items = [p.value for p in processes if p.value is not None]

        logger.info(f"Время: {self.buffer.env.now}, стратегия получила {len(items)} объектов из буфера")
        return items

    def put_buffer_items(self, items: Union[List[Part], Part], **kwargs):
        """Поместить объекты в Store"""
        if self.buffer is None:
            logger.error(f"Буфер не установлен для стратегии")
            raise ValueError("Буфер не установлен для стратегии")

        if not isinstance(items, list):
            logger.debug(f"На загрузку подана одна деталь, помещаем ее в список")
            items = [items]

        logger.info(f"Время: {self.buffer.env.now}, стратегия загружает объекты в буфер")

        # Создаем процессы для каждого помещения
        processes = [self.buffer.env.process(self.buffer.put_item(item, **kwargs)) for item in items]

        # Ждем завершения всех процессов
        yield simpy.AllOf(self.buffer.env, processes)

        logger.info(f"Время: {self.buffer.env.now}, стратегия поместила {len(items)} объектов в буфер")

    def __repr__(self) -> str:
        return f"StoreBatchStrategies(buffer={self.buffer}, batch_size={self.batch_size})"

    def __str__(self) -> str:
        return (f"buffer={self.buffer}\n"
                f"batch_size={self.batch_size}\n")


class ContainerBatchStrategies(Strategies):
    """Стратегия для BufferContainer (работы с количествами)"""

    def __init__(self, buffer: BufferContainer, batch_size: Union[int, float] = 1):
        self.batch_size = batch_size # Размер партии
        self.buffer = buffer # Буфер с которым взаимодействуем

    def get_buffer_items(self, count: Optional[Union[int, float]]= None, **kwargs):
        """Получить количество из Container"""
        if self.buffer is None:
            logger.error(f"Буфер не установлен для стратегии")
            raise ValueError("Буфер не установлен для стратегии")

        if count is None:
            logger.debug(f"Установлен стандартный объем партии")
            count = self.batch_size

        if count <= 0:
            logger.error(f"Количество должно быть больше 0")
            raise ValueError("Количество должно быть больше 0")

        logger.info(f"Время: {self.buffer.env.now}, стратегия ожидает объекты из буфера")

        # Создаем процесс для получения
        process = self.buffer.env.process(self.buffer.get_item(count, **kwargs))
        yield process

        actual_count = process.value if process.value is not None else 0

        logger.info(f"Время: {self.buffer.env.now}, стратегия получила {actual_count} единиц")
        return actual_count

    def put_buffer_items(self, items: Any, **kwargs):
        """Поместить количество в Container"""
        if self.buffer is None:
            logger.error(f"Буфер не установлен для стратегии")
            raise ValueError("Буфер не установлен для стратегии")

        # Определяем количество для помещения
        quantity: Union[int, float]
        if isinstance(items, list):
            logger.debug(f"На загрузку получен список, загружаем количество объектов в списке")
            quantity = len(items)
        elif isinstance(items, (int, float)):
            logger.debug(f"На загрузку получен int/float")
            quantity = items
        else:
            logger.debug(f"Не корректный тип передаваемого количества объектов, установлено значение 1")
            quantity = 1

        if quantity <= 0:
            logger.error(f"Количество должно быть больше 0")
            raise ValueError("Количество должно быть больше 0")

        logger.info(f"Время: {self.buffer.env.now}, стратегия ожидает объекты из буфера")

        yield from self.buffer.put_item(quantity, **kwargs)

        logger.info(f"Время: {self.buffer.env.now}, стратегия поместила {quantity} единиц")

    def __repr__(self) -> str:
        return f"ContainerBatchStrategies(buffer={self.buffer}, batch_size={self.batch_size})"

    def __str__(self) -> str:
        return (f"buffer={self.buffer}\n"
                f"batch_size={self.batch_size}\n")


class StoreAssemblingStrategies(Strategies):
    def __init__(self, buffer: BufferStore):
        self.buffer = buffer # Буфер с которым взаимодействуем

    def get_buffer_items(self, assembly_components: Dict[str, int], **kwargs):
        processes = []

        for component_type, quantity in assembly_components.items():
            # Создаем фильтр для конкретного типа компонента
            filter_func = lambda part, ct=component_type: part.part_config.name == ct

            # Получаем нужное количество компонентов нужного типа
            for _ in range(quantity):
                processes.append(self.buffer.env.process(self.buffer.get_item(filter_item=filter_func, **kwargs)))

        yield simpy.AllOf(self.buffer.env, processes)

        # Возвращаем полученные компоненты
        return [process.value for process in processes if process.value is not None]

    def put_buffer_items(self, items: List[Part], **kwargs):
        assembly_part = Part(PartConfig(name="Сборочная единица", metadata={"assembly_components": items}))

        yield from self.buffer.put_item(assembly_part)

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...


class ContainerAssemblingStrategies(Strategies):
    def __init__(self, buffer: BufferContainer, assembly_components: Dict[str, Union[int, float]]):
        self.buffer = buffer  # Буфер с которым взаимодействуем
        self.assembly_components = assembly_components  # Словарь компонентов требуемых для сборки

    def get_buffer_items(self, **kwargs):
        ...


    def put_buffer_items(self, items: Part, **kwargs):
        ...

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...