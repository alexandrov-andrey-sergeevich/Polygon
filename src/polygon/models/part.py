import logging
from ..utils.validators import PartConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Part:
    def __init__(self, part_config: PartConfig):
        self.part_config = part_config

    def __repr__(self):
        return f"Part({self.part_config})"

    def __str__(self):
        return (f"id: {self.part_config.id}\n"
                f"name: {self.part_config.name}\n"
                f"path: {self.part_config.path}\n"
                f"metadata: {self.part_config.metadata}\n")
