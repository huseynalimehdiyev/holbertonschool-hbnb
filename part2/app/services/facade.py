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


    def get_user(self, user_id):
        return self.user_repo.get(user_id)

 
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

  
    def create_review(self, data):
        # validate relations
        user = self.get_user(data["user_id"])
        place = self.get_place(data["place_id"])

        if not user or not place:
            return None

        review = Review(**data)
        created = self.review_repo.create(review)

        # attach review to place
        if not hasattr(place, "reviews"):
            place.reviews = []

        place.reviews.append(created.id)

        return created

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, data):
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)


facade = HBnBFacade()