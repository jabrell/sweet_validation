import json
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from sweet_validation.schema_manager import SchemaManager

from .schemas import invalid_schema, valid_schema


def test_validate_schema_from_dict():
    relation_manager = SchemaManager()
    assert relation_manager.validate_schema(valid_schema) is None
    # invalid schema should raise a validation error
    with pytest.raises(ValidationError):
        relation_manager.validate_schema(invalid_schema)
    relation_manager.clear_and_close()


def test_validate_schema_from_json(fn: str = "schema.json"):
    relation_manager = SchemaManager()
    # write schema to json file
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(valid_schema, f)
    assert relation_manager.validate_schema(my_file) is None
    my_file.unlink()
    # invalid schema should raise a validation error
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(invalid_schema, f)
    with pytest.raises(ValidationError):
        relation_manager.validate_schema(my_file)
    my_file.unlink()
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", ["schema.yaml", "schema.yml"])
def test_validate_schema_from_yaml(fn: str):
    relation_manager = SchemaManager()
    # write schema to json file
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(valid_schema, f)
    assert relation_manager.validate_schema(my_file) is None
    my_file.unlink()
    # invalid schema should raise a validation error
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(invalid_schema, f)
    with pytest.raises(ValidationError):
        relation_manager.validate_schema(my_file)
    my_file.unlink()
    relation_manager.clear_and_close()
