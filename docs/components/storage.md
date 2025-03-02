## Storage

Storage is responsible to store received data. It is characterized by a simple Protocol
that allows to store, retrieve, and replace data.

## API Docs

### Storage Protocol

::: sweet_validation.protocols.StorageProtocol

### InMemoryStorage

The InMemoryStorage class is a simple storage that uses a dictionary to store your
data. As data are not persisted, its main use case is testing.

::: sweet_validation.storage.InMemoryStorage