class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def get_all(self):
        return list(self.storage.values())
