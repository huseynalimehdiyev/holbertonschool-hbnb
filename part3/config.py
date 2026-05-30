class Config:
    SECRET_KEY = "super-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-key"