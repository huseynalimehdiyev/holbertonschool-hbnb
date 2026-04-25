from flask_restx import Namespace, Resource
from flask import request
from app.services.facade import facade

api = Namespace('users', description="User operations")

@api.route('/')
class UserList(Resource):
    def get(self):
        users = facade.get_users()
        return [u.__dict__ for u in users]

    def post(self):
        data = request.json
        user = facade.create_user(data)
        return user.__dict__, 201


@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "Not found"}, 404
        return user.__dict__

    def put(self, user_id):
        data = request.json
        user = facade.update_user(user_id, data)
        if not user:
            return {"error": "Not found"}, 404
        return user.__dict__

    def delete(self, user_id):
        facade.delete_user(user_id)
        return {"message": "Deleted"}