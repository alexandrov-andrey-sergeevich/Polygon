import json
from typing import Type
from pathlib import Path
from pydantic import BaseModel


def generator_json_schema(
        model: Type[BaseModel],
        output_dir: str | Path,
        filename: str
) -> Path:
    if not isinstance(model, type) or not issubclass(model, BaseModel):
        raise TypeError(f"Ожидается объект типа BaseModel, получен: {type(model)}")

    if not isinstance(output_dir, Path):
        output_dir: Path = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    schema = model.model_json_schema()

    output_file = output_dir / f"{filename}.schema.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    return output_file
