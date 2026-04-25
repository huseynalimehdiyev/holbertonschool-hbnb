from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/')
class AmenityList(Resource):

    def get(self):
        amenities = facade.get_all_amenities()
        return [a.__dict__ for a in amenities], 200

    @api.expect(amenity_model)
    def post(self):
        data = request.json
        try:
            amenity = facade.create_amenity(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return amenity.__dict__, 201


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):

    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.__dict__, 200

    @api.expect(amenity_model)
    def put(self, amenity_id):
        data = request.json
        try:
            amenity = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.__dict__, 200