from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        super().__init__()

        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)

        self.user_id = user_id
        self.place_id = place_id

    def validate_text(self, text):
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        return text

    def validate_rating(self, rating):
        rating = float(rating)
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating