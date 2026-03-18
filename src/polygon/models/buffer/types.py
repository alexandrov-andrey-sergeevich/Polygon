"""
Используется для полиморфной обработки разных типов буферов
через дискриминатор 'buffer_type'
"""

from typing import Annotated
from pydantic import Field
from .discrete import DiscreteBufferConfig
from .bulk import BulkBufferConfig


BufferConfig = Annotated[
    DiscreteBufferConfig | BulkBufferConfig,
    Field(discriminator="buffer_type")
]
