from typing import Annotated
from pydantic import Field
from .source import SourceConfig
from .simple import SimpleConfig
from .combining import CombiningConfig
from .sink import SinkConfig


ProcessConfig = Annotated[
    SourceConfig | SimpleConfig | CombiningConfig | SinkConfig,
    Field(discriminator="object_type")
]
