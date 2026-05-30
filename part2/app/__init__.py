from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from config import Config

bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    bcrypt.init_app(app)

    api = Api(app, title="HBnB API", version="1.0")

    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns

    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(reviews_ns, path="/reviews")
    api.add_namespace(amenities_ns, path="/amenities")

    return app