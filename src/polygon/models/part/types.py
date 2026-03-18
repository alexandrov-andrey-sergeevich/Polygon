"""
Используется для полиморфной обработки разных типов деталей
через дискриминатор 'part_type'
"""

from typing import Annotated
from pydantic import Field
from .discrete import DiscretePartConfig
from .bulk import BulkPartConfig
from .assembly import AssemblyPartConfig
from .mixture import MixturePartConfig


PartConfig = Annotated[
    DiscretePartConfig | BulkPartConfig | AssemblyPartConfig | MixturePartConfig,
    Field(discriminator="part_type")
]
