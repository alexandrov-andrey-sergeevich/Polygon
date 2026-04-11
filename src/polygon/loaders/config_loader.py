import json
from typing import Any
from pathlib import Path
from jsonschema import Draft7Validator


class ConfigLoader:
    @staticmethod
    def _load_json(path: str | Path) -> dict[str, Any]:
        if path is None:
            raise ValueError("Путь к файлу не указан")

        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")

        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError as e:
                raise ValueError(f"Ошибка парсинга json файла: {e}")

    @staticmethod
    def _validate_config(data: dict[str, Any], schema: dict[str, Any]) -> None:
        Draft7Validator(schema).validate(data)

    def load(self, config_path: str | Path, schema_path: str | Path, validate: bool = True) -> dict[str, Any]:
        config = self._load_json(config_path)
        schema = self._load_json(schema_path)

        if validate:
            self._validate_config(config, schema)
        return config

