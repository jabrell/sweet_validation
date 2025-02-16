import json
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore


def read_schema_from_file(file: str | Path | dict[str, Any]) -> dict[str, Any]:
    """Read a file in either json or yaml format

    Args:
        file (str | Path): File path

    Returns:
        dict: File contents

    Raises:
        ValueError: If file is not json or yaml (.json, .yaml, .yml)
        FileNotFoundError: If file is not found
    """
    if isinstance(file, dict):
        return file
    file = Path(file)
    with open(file) as f:
        if file.suffix == ".json":
            return cast(dict[str, Any], json.load(f))
        elif file.suffix in [".yaml", ".yml"]:
            return cast(dict[str, Any], yaml.safe_load(f))
        else:
            raise ValueError(
                f"File {file} is not json or yaml. Use .json, .yaml, or .yml"
            )
