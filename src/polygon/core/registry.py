from typing import Type, Any
from .context import SimulationContext

class ComponentRegistry:
    _mapping: dict[str, Type] = {}

    @classmethod
    def registry(cls, object_type: str) -> Any:
        def decorator(component_cls):
            cls._mapping[object_type] = component_cls
            return component_cls
        return decorator

    @classmethod
    def create(cls, config_obj: Any, context: SimulationContext) -> Any:
        obj_type = config_obj.object_type
        component_cls = cls._mapping.get(obj_type)

        if component_cls is None:
            raise ValueError(f"Неизвестный тип объекта: {obj_type}")
        return component_cls(config_obj, context)
