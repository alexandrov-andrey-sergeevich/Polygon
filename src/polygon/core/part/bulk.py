from src.polygon.models.part.bulk import BulkPartConfig


class BulkPart:
    """Непрерывный материал (сыпучие, жидкости, газы)"""
    def __init__(self, config: BulkPartConfig):
        self.config = config
