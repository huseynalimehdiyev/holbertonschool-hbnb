from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    # USER METHODS
    def create_user(self, data):
        user = User(**data)
        return self.user_repo.create(user)

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)


facade = HBnBFacade()