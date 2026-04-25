from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String)
})

@api.route('/')
class PlaceList(Resource):

    def get(self):
        places = facade.get_all_places()

        result = []
        for p in places:
            owner = facade.get_user(p.owner_id)

            result.append({
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner": owner.__dict__ if owner else None,
                "amenities": p.amenities,
                "reviews": p.reviews if hasattr(p, "reviews") else []
            })

        return result, 200

    @api.expect(place_model)
    def post(self):
        data = request.json
        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return place.__dict__, 201


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner.__dict__ if owner else None,
            "amenities": place.amenities,
            "reviews": place.reviews if hasattr(place, "reviews") else []
        }, 200

    @api.expect(place_model)
    def put(self, place_id):
        data = request.json
        try:
            place = facade.update_place(place_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not place:
            return {"error": "Place not found"}, 404

        return place.__dict__, 200