from app.models.base_model import BaseModel
from app import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = self.validate_email(email)

        # 🔥 hashed password (secure storage)
        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        self.is_admin = is_admin

    # ======================
    # EMAIL VALIDATION
    # ======================
    def validate_email(self, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        return email

    # ======================
    # PASSWORD CHECK
    # ======================
    def verify_password(self, password):
        return bcrypt.check_password_hash(
            self.password,
            password
        )

    # ======================
    # UPDATE USER
    # ======================
    def update(self, data):
        for key, value in data.items():

            # ❌ email validation
            if key == "email":
                value = self.validate_email(value)

            # 🔥 password re-hash
            if key == "password":
                value = bcrypt.generate_password_hash(
                    value
                ).decode("utf-8")

            # ❌ security: prevent role override unless admin (handled in API)
            if key == "is_admin":
                continue

            if hasattr(self, key):
                setattr(self, key, value)

        self.save()