from app.models.base_model import BaseModel, db


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False)

    # Relationships will be added later (Place ↔ Amenity M2M)

    def update(self, data):
        for key, value in data.items():

            if key == "name":
                value = self.validate_name(value)

            if hasattr(self, key):
                setattr(self, key, value)

        db.session.commit()

    # ======================
    # VALIDATION
    # ======================
    def validate_name(self, name):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        return name