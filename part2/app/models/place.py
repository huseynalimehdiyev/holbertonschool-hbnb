from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None):
        super().__init__()

        # basic fields
        self.title = title
        self.description = description

        # validation
        self.price = float(price)
        self.latitude = self.validate_lat(latitude)
        self.longitude = self.validate_long(longitude)

        # relationships
        self.owner_id = owner_id
        self.amenities = amenities if amenities else []

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

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()