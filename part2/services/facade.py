from persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.repo = InMemoryRepository()

    def add_object(self, obj):
        self.repo.add(obj)

    def get_object(self, obj_id):
        return self.repo.get(obj_id)

    def get_all_objects(self):
        return self.repo.get_all()