from typing import Annotated
from pydantic import Field
from .bulk import BulkBufferConfig
from .discrete import DiscreteBufferConfig


BufferConfig = Annotated[
    BulkBufferConfig | DiscreteBufferConfig,
    Field(discriminator="object_type")
]
