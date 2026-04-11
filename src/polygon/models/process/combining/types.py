from typing import Annotated
from pydantic import Field
from .mixing import MixingProcessConfig
from .assembly import AssemblyProcessConfig


CombiningConfig = Annotated[
    MixingProcessConfig | AssemblyProcessConfig,
    Field(discriminator="object_type")
]
