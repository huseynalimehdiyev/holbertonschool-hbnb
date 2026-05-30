from app.models.base_model import BaseModel, db


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(60), nullable=False)
    place_id = db.Column(db.String(60), nullable=False)

    # ❌ Relationships will be added later (Place, User)

    def update(self, data):
        for key, value in data.items():
            # validation helpers
            if key == "text":
                value = self.validate_text(value)
            elif key == "rating":
                value = self.validate_rating(value)

            if hasattr(self, key):
                setattr(self, key, value)

        db.session.commit()

    # ======================
    # VALIDATION HELPERS
    # ======================

    def validate_text(self, text):
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        return text

    def validate_rating(self, rating):
        rating = float(rating)
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating