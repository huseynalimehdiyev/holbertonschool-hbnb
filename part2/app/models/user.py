from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def validate_email(self, email):
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()