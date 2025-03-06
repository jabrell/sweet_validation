from pathlib import Path

import pandas as pd
import pytest
from faker import Faker

from sweet_validation.exceptions import DataValidationError
from sweet_validation.registry import InMemoryRegistry
from sweet_validation.schema_manager import SchemaManager
from sweet_validation.utils import read_schema_from_file
from sweet_validation.validator.default import DefaultValidator

fn_schema = BASE_SCHEMA = Path(__file__).parent / "data" / "example_generation.yaml"


def test_add_schema():
    man = SchemaManager()
    man.add_schema("generation", fn_schema)
    assert man["generation"] == read_schema_from_file(fn_schema)
    man.clear_and_close()


def test_data_validation():
    schema_key = "generation"
    length = 10
    fake = Faker()
    registry = InMemoryRegistry(
        validator=DefaultValidator(), schema_manager=SchemaManager()
    )
    registry.add_schema(schema_key, fn_schema)
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2021-01-01", periods=length, freq="h"),
            "country": [fake.country() for _ in range(length)],
            "value": [i + 1 for i in range(length)],
        }
    )
    registry.add_data("generation_test", schema_key="generation", data=df)
    # violate the minimum value restriction
    df.loc[0, "value"] = -1
    with pytest.raises(DataValidationError):
        registry.add_data("generation_test_false", schema_key="generation", data=df)
