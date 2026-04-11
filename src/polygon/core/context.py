from typing import Any
from uuid import UUID
import simpy


class SimulationContext:
    def __init__(self, env: simpy.Environment):
        self.env = env
        self._components: dict[UUID, Any] = {}

    def register_component(self, uuid: UUID, component: Any) -> None:
        """Зарегистрировать компонент в общем реестре"""
        self._components[uuid] = component

    def get_component(self, uuid: UUID) -> Any | None:
        """Получить компонент по UUID"""
        return self._components.get(uuid)

    def get_components_by_type(self, object_type: str) -> list[Any]:
        """Вернуть все компоненты с указанным object_type (если они хранят свой тип)."""
        return [
            comp for comp in self._components.values()
            if hasattr(comp, "config") and getattr(comp.config, "object_type", None) == object_type
        ]
