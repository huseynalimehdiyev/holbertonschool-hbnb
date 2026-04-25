from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace('users', description='User operations')

# DTO (validation + documentation)
user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True)
})

# -------------------------
# POST + GET ALL
# -------------------------
@api.route('/')
class UserList(Resource):

    # GET /users/
    def get(self):
        users = facade.get_all_users()

        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email
                # ❌ password yoxdur (important!)
            }
            for u in users
        ], 200

    # POST /users/
    @api.expect(user_model)
    def post(self):
        data = request.json
        user = facade.create_user(data)

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 201


@api.route('/<string:user_id>')
class UserResource(Resource):

    # GET /users/id
    def get(self, user_id):
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200

    # PUT /users/id
    @api.expect(user_model)
    def put(self, user_id):
        data = request.json
        user = facade.update_user(user_id, data)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200