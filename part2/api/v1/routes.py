from flask import Blueprint, request
from services.facade import HBnBFacade
from models.user import User

api = Blueprint('api', __name__)

facade = HBnBFacade()


@api.route('/test')
def test():
    return {"message": "API working"}


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or "name" not in data:
        return {"error": "Name is required"}, 400

    user = User(data["name"])
    facade.add_object(user)

    return {"id": user.id, "name": user.name}, 201


@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = facade.get_object(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {"id": user.id, "name": user.name}