import uuid

class InMemoryRepository:
    def __init__(self):
        self.data = {}

    def get_all(self):
        return list(self.data.values())

    def get(self, obj_id):
        return self.data.get(obj_id)

    def create(self, obj):
        obj.id = str(uuid.uuid4())
        self.data[obj.id] = obj
        return obj

    def update(self, obj_id, new_data):
        if obj_id in self.data:
            for key, value in new_data.items():
                setattr(self.data[obj_id], key, value)
            return self.data[obj_id]
        return None

    def delete(self, obj_id):
        return self.data.pop(obj_id, None)