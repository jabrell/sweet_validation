import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore


def read_json_or_yaml(file: str | Path) -> dict[str, Any]:
    """Read a file in either json or yaml format

    Args:
        file (str | Path): File path

    Returns:
        dict: File contents

    Raises:
        ValueError: If file is not json or yaml (.json, .yaml, .yml)
        FileNotFoundError: If file is not found
    """
    file = Path(file)
    with open(file) as f:
        if file.suffix == ".json":
            return json.load(f)  # type: ignore
        elif file.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(f)  # type: ignore
        else:
            raise ValueError(
                f"File {file} is not json or yaml. Use .json, .yaml, or .yml"
            )
