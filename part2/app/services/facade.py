from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

    # ---------------- USERS ----------------
    def create_user(self, data):
        user = User(**data)
        return self.user_repo.create(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    # ---------------- AMENITIES ----------------
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    # ---------------- PLACES ----------------
    def create_place(self, data):
        place = Place(**data)
        return self.place_repo.create(place)

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)


facade = HBnBFacade()