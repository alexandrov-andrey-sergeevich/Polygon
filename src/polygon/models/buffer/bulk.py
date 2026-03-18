from typing import Literal
from pydantic import Field
from .base import BaseBufferConfig


class BulkBufferConfig(BaseBufferConfig):
    """
    Буфер с непрерывным типом объектов, измеряемых в объеме или массе:
        - жидкости (вода, масло, топливо)
        - сыпучие материалы (песок, цемент, зерно)
        - газы (воздух, азот, аргон)

    Отличается от дискретного буфера тем, что хранит непрерывную величину.
    """
    buffer_type: Literal["bulk"] = Field(
        default="bulk",
        description="Тип буфера: непрерывная величина."
    )