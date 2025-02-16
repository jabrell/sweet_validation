import json
from pathlib import Path

import pytest
import yaml

from sweet_validation.utils import read_schema_from_file


def test_read_json():
    content = {"key": "value"}
    fn = Path("tmp.json")
    with open(fn, "w") as f:
        json.dump(content, f)
    assert read_schema_from_file(fn) == content
    Path(fn).unlink()


@pytest.mark.parametrize("ext", [".yaml", ".yml"])
def test_read_yaml(ext: str):
    content = {"key": "value"}
    fn = Path(f"tmp.{ext}")
    with open(fn, "w") as f:
        yaml.dump(content, f)
    assert read_schema_from_file(fn) == content
    fn.unlink()


def test_read_invalid():
    fn = Path("tmp.txt")
    with open(fn, "w") as f:
        f.write("invalid")
    with pytest.raises(ValueError):
        read_schema_from_file(fn)
    fn.unlink()
    # file not found
    with pytest.raises(FileNotFoundError):
        read_schema_from_file(fn)
