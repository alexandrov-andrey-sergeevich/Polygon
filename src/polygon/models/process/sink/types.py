from typing import Annotated
from pydantic import Field
from .bulk import BulkSinkConfig
from .discrete import DiscreteSinkConfig


SinkConfig = Annotated[
    BulkSinkConfig | DiscreteSinkConfig,
    Field(discriminator="object_type")
]
