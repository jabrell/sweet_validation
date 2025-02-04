from faker import Faker

from sweet_validation.validation import validate_csv_file

if __name__ == "__main__":
    fake = Faker()
    fn_scheme = "scheme.yaml"
    fn_valid = "valid.csv"
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

    with open(fn_valid, "w") as f:
        f.write("name,year,value\n")
        f.write(f"{fake.name()},{fake.name()},{fake.random_int()}\n")
        f.write(f"{fake.name()},{fake.name()},{fake.random_int()}\n")
    validate_csv_file(fn_valid, fn_scheme)
