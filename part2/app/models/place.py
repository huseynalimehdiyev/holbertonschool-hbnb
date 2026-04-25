from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.owner_id = owner_id

        # relationships
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()