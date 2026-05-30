from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ======================
    # USERS
    # ======================

    def create_user(self, data):
        """
        Create a new user
        Only admin can create another admin
        """
        is_admin = data.get("is_admin", False)
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            is_admin=is_admin
        )
        return self.user_repo.create(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data, admin_override=False):
        """
        Update user data.
        Normal users cannot change email, password, or is_admin
        Admins can update everything
        """
        user = self.get_user(user_id)
        if not user:
            return None

        if not admin_override:
            data.pop("email", None)
            data.pop("password", None)
            data.pop("is_admin", None)

        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        for user in self.user_repo.get_all():
            if user.email == email:
                return user
        return None

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

    def update_place(self, place_id, data, admin_override=False, user_id=None):
        """
        Normal user can only update own places
        Admins can update any place
        """
        place = self.get_place(place_id)
        if not place:
            return None

        if not admin_override and getattr(place, "owner_id", None) != user_id:
            raise PermissionError("You cannot modify a place you do not own")

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

        # ❌ cannot review own place
        if getattr(place, "owner_id", None) == data["user_id"]:
            raise ValueError("You cannot review your own place")

        # ❌ duplicate review prevention
        for r in self.review_repo.get_all():
            if r.user_id == data["user_id"] and r.place_id == data["place_id"]:
                raise ValueError("You already reviewed this place")

        review = Review(**data)
        created = self.review_repo.create(review)

        # link review to place
        if not hasattr(place, "reviews"):
            place.reviews = []

        place.reviews.append(created.id)

        return created

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data, admin_override=False, user_id=None):
        """
        Normal user can only update own reviews
        Admins can update any review
        """
        review = self.get_review(review_id)
        if not review:
            return None

        if not admin_override and review.user_id != user_id:
            raise PermissionError("You cannot modify a review you do not own")

        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id, admin_override=False, user_id=None):
        """
        Normal user can only delete own reviews
        Admins can delete any review
        """
        review = self.get_review(review_id)
        if not review:
            return False

        if not admin_override and review.user_id != user_id:
            raise PermissionError("You cannot delete a review you do not own")

        return self.review_repo.delete(review_id)


# singleton facade
facade = HBnBFacade()