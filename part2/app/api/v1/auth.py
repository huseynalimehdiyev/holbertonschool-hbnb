from flask_restx import Namespace, Resource
from flask import request

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.services.facade import facade

api = Namespace(
    "auth",
    description="Authentication operations"
)


# ======================
# LOGIN
# ======================
@api.route("/login")
class Login(Resource):

    def post(self):

        data = request.get_json()

        # 🔥 safer validation
        if not data or "email" not in data or "password" not in data:
            return {"error": "Missing credentials"}, 400

        email = data.get("email")
        password = data.get("password")

        user = facade.get_user_by_email(email)

        # ❌ invalid credentials (generic response is correct)
        if not user or not user.verify_password(password):
            return {"error": "Invalid credentials"}, 401

        # 🔥 JWT with role info
        token = create_access_token(
            identity=user.id,
            additional_claims={
                "is_admin": user.is_admin
            }
        )

        return {"access_token": token}, 200


# ======================
# PROTECTED ROUTE
# ======================
@api.route("/protected")
class Protected(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        return {
            "message": "Access granted",
            "user_id": user_id
        }, 200