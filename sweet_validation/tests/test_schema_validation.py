import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError

from sweet_validation.schema_manager import SchemaManager

# valid and invalid schema under frictionless standard only
fl_valid = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
}

fl_invalid = {"name": "test"}


def test_validate_schema_from_dict():
    relation_manager = SchemaManager(metaschema_extensions=[])
    assert relation_manager.validate_schema(fl_valid) is None
    # invalid schema should raise a validation error
    with pytest.raises(ValidationError):
        relation_manager.validate_schema(fl_invalid)
    relation_manager.clear_and_close()


def test_validate_schema_from_json(fn: str = "schema.json"):
    relation_manager = SchemaManager(metaschema_extensions=[])
    # write schema to json file
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(fl_valid, f)
    assert relation_manager.validate_schema(my_file) is None
    my_file.unlink()
    # invalid schema should raise a validation error
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(fl_invalid, f)
    with pytest.raises(ValidationError):
        relation_manager.validate_schema(my_file)
    my_file.unlink()
    relation_manager.clear_and_close()


@pytest.mark.parametrize("fn", ["schema.yaml", "schema.yml"])
def test_validate_schema_from_yaml(fn: str):
    relation_manager = SchemaManager(metaschema_extensions=[])
    # write schema to json file
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(fl_valid, f)
    assert relation_manager.validate_schema(my_file) is None
    my_file.unlink()
    # invalid schema should raise a validation error
    my_file = Path(fn)
    with open(my_file, "w") as f:
        json.dump(fl_invalid, f)
    with pytest.raises(ValidationError):
        relation_manager.validate_schema(my_file)
    my_file.unlink()
    relation_manager.clear_and_close()


def test_sweet_extensions():
    """Test extended metadata standard of SWEET"""
    invalid_schema = {
        # schema misses the "name" key which is mandatory in the SWEET standard
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "string"},
        ],
    }
    man = SchemaManager(metaschema_extensions=[])
    sweet_man = SchemaManager()
    assert man.validate_schema(invalid_schema) is None
    with pytest.raises(ValidationError):
        sweet_man.validate_schema(invalid_schema)


sweet_valid = {
    # schema misses the "name" key which is mandatory in the SWEET standard
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
    "name": "test",
    "title": "test",
    "description": "test",
    "primaryKey": ["test"],
}


def test_sweet_extensions_name_format():
    """Test extended metadata standard of SWEET"""
    schema = deepcopy(sweet_valid)
    schema["name"] = "TEST"
    with pytest.raises(ValidationError):
        SchemaManager().validate_schema(schema)
    schema["name"] = "test!"
    with pytest.raises(ValidationError):
        SchemaManager().validate_schema(schema)
    schema["name"] = "test_test"
    assert SchemaManager().validate_schema(schema) is None

    # name of format of field is also fixed to using lower cases and underscores
    schema["fields"][0]["name"] = "ID"
    with pytest.raises(ValidationError):
        SchemaManager().validate_schema(schema)


def test_sweet_extensions_no_additional_fields():
    """Test extended metadata standard of SWEET"""
    schema = deepcopy(sweet_valid)
    schema["additional"] = "field"
    with pytest.raises(ValidationError):
        SchemaManager().validate_schema(schema)
