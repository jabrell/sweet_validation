from frictionless.fields import IntegerField

from sweet_validation.columns.columns import Column

if __name__ == "__main__":
    field = IntegerField(name="test")
    items = [1, 2, 3]
    col = Column(field=field, items=items)
    print(col)
    print(col.name)
    # assert col.field == field
    # assert col.items == [1, 2, 3]
    print("done")
