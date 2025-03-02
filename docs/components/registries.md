## Registries

Registries coordinate actions between the data and schema storage. They ensure
that no data are stored without a schema and that changes in data trigger a
validation of data against the respective schema.


## API Docs

### In Memory-Registry

The in-memory registry is the simplest registry possible. It uses the standard
Sqlite-based SchemaManager together with an in-memory storage of the data. Therefore,
data will be lost once you stop the Python program, i.e., data are not persisted.

::: sweet_validation.registry.InMemoryRegistry