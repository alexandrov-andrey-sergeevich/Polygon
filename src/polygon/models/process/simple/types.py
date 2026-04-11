from typing import Annotated
from pydantic import Field
from .bulk import BulkSimpleProcessConfig
from .discrete import DiscreteSimpleProcessConfig


SimpleConfig = Annotated[
    BulkSimpleProcessConfig | DiscreteSimpleProcessConfig,
    Field(discriminator="object_type")
]
