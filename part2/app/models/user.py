from app.models.base_model import BaseModel
from app import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = self.validate_email(email)

        # hashed password
        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def validate_email(self, email):
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email

    def verify_password(self, password):
        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def update(self, data):
        for key, value in data.items():

            # email validation
            if key == "email":
                value = self.validate_email(value)

            # password update => rehash
            if key == "password":
                value = bcrypt.generate_password_hash(
                    value
                ).decode("utf-8")

            if hasattr(self, key):
                setattr(self, key, value)

        self.save()