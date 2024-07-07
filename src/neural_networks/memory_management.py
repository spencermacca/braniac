class MemoryManagementNN:
    def __init__(self):
        self.memory_store = {}

    def store_memory(self, key, value):
        if key not in self.memory_store:
            self.memory_store[key] = []
        self.memory_store[key].append(value)
        print(f"Stored {key}: {value}")

    def retrieve_memory(self, key):
        return self.memory_store.get(key, [])

    def retrieve_last_memory(self, key):
        return self.memory_store.get(key, [None])[-1]
