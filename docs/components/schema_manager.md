# SchemaManager

SchemaManagers manage your schemas. They perform the following tasks:

- Ensure that each provided schema complies with the metadata standard provided
- Allow to store and retrieve schemas
- Store the relations between data and schemas

The default SchemaManager uses an Sqlite database to store schemas and relations.

## Metadata Standards

The metadata standard is provided during the initialization of the SchemaManager.
By default, the SchemaManager uses the [frictionless table schema in version 1](https://specs.frictionlessdata.io/table-schema/) with the additional constraint that name of the table
is mandatory.

The metadata standard can be changed in two different ways during initialization
of the SchemaManager

1. Provide your own metadata standard in the form of a json schema
2. Extend the basic metadata standard providing additional json schemas. In that
case, all schemas need to be fulfilled by newly created data schemas. <span style="color:red">TO BE IMPLEMENTED</span>

## API Docs

### SchemaManager

::: sweet_validation.schema_manager.SchemaManager





