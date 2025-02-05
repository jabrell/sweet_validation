"""
TODO: delete me
That is only for testing and playing around with the frictionless library.
should be deleted later on.
"""

from faker import Faker

from sweet_validation.validation import validate_csv_file

tmp_dir = "./sweet_validation/tests/_tmp/"


def test_validate_csv():
    fake = Faker()
    import os

    print(os.getcwd())
    fn_scheme = tmp_dir + "scheme.yaml"
    fn_valid = tmp_dir + "valid.csv"
    with open(fn_scheme, "w") as f:
        f.write("""
fields:
  - name: name
    type: string
  - name: year
    type: integer
  - name: value
    type: number
""")
    with open(fn_valid, "w") as f:
        f.write("name,year,value\n")
        f.write(f"{fake.name()},{fake.year()},{fake.random_int()}\n")
        f.write(f"{fake.name()},{fake.year()},{fake.random_int()}\n")
    assert validate_csv_file(fn_valid, fn_schema=fn_scheme)

    # invalid file
    with open(fn_valid, "w") as f:
        f.write("name,year,value\n")
        f.write(f"{fake.name()},{fake.name()},{fake.random_int()}\n")
        f.write(f"{fake.name()},{fake.name()},{fake.random_int()}\n")
    assert not validate_csv_file(fn_valid, fn_schema=fn_scheme)
