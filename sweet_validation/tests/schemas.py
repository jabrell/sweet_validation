valid_schema = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
    "name": "test",
    "title": "Test",
    "description": "Test",
}

valid_schema2 = {
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
    "name": "test_two",
    "title": "Test",
    "description": "Test",
}

# this schema is missing the "name" key which is required (in addition to "fields")
# in contrast to the original frictionless schema
invalid_schema = {
    # schema misses the "name" key
    "fields": [
        {"name": "id", "type": "integer"},
        {"name": "name", "type": "string"},
    ],
}
