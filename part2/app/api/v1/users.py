from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):

    def get(self):
        users = facade.get_all_users()
        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email
            }
            for u in users
        ], 200

    @api.expect(user_model)
    def post(self):
        data = request.json
        try:
            user = facade.create_user(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return user.__dict__, 201


@api.route('/<string:user_id>')
class UserResource(Resource):

    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.__dict__, 200

    @api.expect(user_model)
    def put(self, user_id):
        data = request.json
        try:
            user = facade.update_user(user_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not user:
            return {"error": "User not found"}, 404

        return user.__dict__, 200
    
@jwt_required()
def put(self, user_id):

    current_user_id = get_jwt_identity()

    if current_user_id != user_id:
        return {
            "error": "Unauthorized action"
        }, 403

    data = request.get_json()

    # email və password dəyişmək olmaz
    data.pop("email", None)
    data.pop("password", None)

    user = facade.update_user(user_id, data)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }, 200