from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def validate_name(self, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        return name

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()