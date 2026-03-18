import logging
import json
from pathlib import Path
from typing import Any, Dict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONLoader:
    @staticmethod
    def load(path: Path | str) -> Dict[str, Any]:
        with open(path, encoding="utf-8") as f:
            json_data = json.load(f)
        return json_data

    @staticmethod
    def save(path: Path | str, json_data: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
