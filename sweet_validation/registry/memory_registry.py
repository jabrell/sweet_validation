from ..storage import MemoryStorage

__all__ = ["MemoryRegistry"]


class MemoryRegistry:
    _schema_store: MemoryStorage
    _data_store: MemoryStorage

    # _relations: MemoryRelationManager

    def __init__(self):
        self._schema_store = MemoryStorage()
        self._data_store = MemoryStorage()
        # self._relations = MemoryRelationManager()

    @property
    def schemas(self) -> list:
        """List of schema keys"""
        return self._schema_store.list()

    @property
    def data(self) -> list:
        """List of data keys"""
        return self._data_store.list()

    def get_schema(self, key: str):
        return self._schema_store.load(key)

    def save_schema(self, key: str, schema):
        self._schema_store.save(key, schema)

    def delete_schema(self, key: str):
        self._schema_store.delete(key)

    def replace_schema(self, key: str, schema):
        self._schema_store.replace(key, schema)

    def get_data(self, key: str):
        return self._data_store.load(key)

    def save_data(self, key: str, data):
        self._data_store.save(key, data)

    def delete_data(self, key: str):
        self._data_store.delete(key)

    def replace_data(self, key: str, data):
        self._data_store.replace(key, data)
