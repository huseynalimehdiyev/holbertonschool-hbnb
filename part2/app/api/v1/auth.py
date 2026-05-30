from flask_restx import Namespace, Resource
from flask import request

from flask_jwt_extended import (
    create_access_token
)

from flask_jwt_extended import jwt_required

from app.services.facade import facade

api = Namespace(
    "auth",
    description="Authentication operations"
)


@api.route("/login")
class Login(Resource):

    def post(self):

        data = request.get_json()

        if not data:
            return {
                "error": "Missing JSON data"
            }, 400

        email = data.get("email")
        password = data.get("password")

        user = facade.get_user_by_email(email)

        if not user:
            return {
                "error": "Invalid credentials"
            }, 401

        if not user.verify_password(password):
            return {
                "error": "Invalid credentials"
            }, 401

        token = create_access_token(
            identity=user.id,
            additional_claims={
                "is_admin": user.is_admin
            }
        )

        return {
            "access_token": token
        }, 200

@api.route("/protected")
class Protected(Resource):

    @jwt_required()
    def get(self):

        return {
            "message": "Access granted"
        }, 200