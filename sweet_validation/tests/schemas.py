valid_schema = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
    "name": "test",
}

valid_schema2 = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
    "name": "test2",
}

# this schema is missing the "name" key which is required (in addition to "fields")
# in contrast to the original frictionless schema
invalid_schema = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
}
