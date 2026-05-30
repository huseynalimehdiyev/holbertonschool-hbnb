from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ======================
    # USERS
    # ======================

    def create_user(self, data):
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"]
        )
        return self.user_repo.create(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    # ======================
    # PLACES
    # ======================

    def create_place(self, data):
        place = Place(**data)
        return self.place_repo.create(place)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        return self.place_repo.update(place_id, data)

    # ======================
    # AMENITIES
    # ======================

    def create_amenity(self, data):
        amenity = Amenity(**data)
        return self.amenity_repo.create(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)

    # ======================
    # REVIEWS
    # ======================

    def create_review(self, data):
        user = self.get_user(data["user_id"])
        place = self.get_place(data["place_id"])

        if not user or not place:
            raise ValueError("Invalid user_id or place_id")

        review = Review(**data)
        created = self.review_repo.create(review)

        if not hasattr(place, "reviews"):
            place.reviews = []

        place.reviews.append(created.id)

        return created

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)


facade = HBnBFacade()