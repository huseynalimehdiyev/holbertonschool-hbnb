from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns

jwt = JWTManager()

def create_app(config_object=None):
    app = Flask(__name__)

    # Config
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    if config_object:
        app.config.from_object(config_object)

    # Initialize JWT
    jwt.init_app(app)

    @jwt.unauthorized_loader
    def missing_token(err):
        return jsonify({"error": "Missing or invalid token"}), 401

    @jwt.invalid_token_loader
    def invalid_token(err):
        return jsonify({"error": "Invalid token"}), 401

    @jwt.expired_token_loader
    def expired_token(header, payload):
        return jsonify({"error": "Token has expired"}), 401

    # RESTx API
    api = Api(app, title="HBnB API", version="1.0")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(reviews_ns, path="/reviews")
    api.add_namespace(amenities_ns, path="/amenities")
    api.add_namespace(auth_ns, path="/auth")

    return app