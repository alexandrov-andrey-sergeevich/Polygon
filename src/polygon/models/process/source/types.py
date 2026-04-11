from typing import Annotated
from pydantic import Field
from .bulk import BulkSourceConfig
from .discrete import DiscreteSourceConfig


SourceConfig = Annotated[
    BulkSourceConfig | DiscreteSourceConfig,
    Field(discriminator="object_type")
]
