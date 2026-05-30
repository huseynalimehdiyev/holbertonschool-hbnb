from app.models.base_model import BaseModel, db


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)

    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(60), nullable=False)
    # ❌ Relationships (reviews, amenities) will be added later

    # ======================
    # UPDATE METHOD
    # ======================
    def update(self, data):
        for key, value in data.items():

            if key == "latitude":
                value = self.validate_lat(value)
            elif key == "longitude":
                value = self.validate_long(value)
            elif key == "price":
                value = self.validate_price(value)

            if hasattr(self, key):
                setattr(self, key, value)

        db.session.commit()

    # ======================
    # VALIDATION HELPERS
    # ======================
    def validate_lat(self, lat):
        lat = float(lat)
        if lat < -90 or lat > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return lat

    def validate_long(self, lon):
        lon = float(lon)
        if lon < -180 or lon > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return lon

    def validate_price(self, price):
        price = float(price)
        if price < 0:
            raise ValueError("Price must be positive")
        return price