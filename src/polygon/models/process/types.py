"""
Используется для полиморфной обработки разных типов деталей
через дискриминатор 'process_type'
"""

from typing import Annotated
from pydantic import Field
from .simple import SimpleProcessConfig
from .assembling import AssemblingProcessConfig
from .disassembling import DisassemblingProcessConfig
from .mixing import MixingProcessConfig

ProcessConfig = Annotated[
    SimpleProcessConfig | AssemblingProcessConfig | DisassemblingProcessConfig | MixingProcessConfig,
    Field(discriminator="process_type")
]
