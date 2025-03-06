from pathlib import Path

from faker import Faker  # noqa

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
    # fake = Faker()
    registry = InMemoryRegistry(
        validator=DefaultValidator(), schema_manager=SchemaManager()
    )
    print(registry)
