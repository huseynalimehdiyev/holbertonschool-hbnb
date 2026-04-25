from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})


@api.route('/')
class AmenityList(Resource):

    # GET /amenities/
    def get(self):
        amenities = facade.get_all_amenities()

        return [
            {
                "id": a.id,
                "name": a.name
            }
            for a in amenities
        ], 200

    # POST /amenities/
    @api.expect(amenity_model)
    def post(self):
        data = request.json
        amenity = facade.create_amenity(data)

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 201



@api.route('/<string:amenity_id>')
class AmenityResource(Resource):

    # GET /amenities/<id>
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 200

    # PUT /amenities/<id>
    @api.expect(amenity_model)
    def put(self, amenity_id):
        data = request.json
        amenity = facade.update_amenity(amenity_id, data)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 200