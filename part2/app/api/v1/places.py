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
    'amenities': fields.List(fields.String, required=False)
})

@api.route('/')
class PlaceList(Resource):

    # GET /places/
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

                # owner details (IMPORTANT REQUIREMENT)
                "owner": {
                    "id": owner.id if owner else None,
                    "first_name": owner.first_name if owner else None,
                    "last_name": owner.last_name if owner else None
                },

                "amenities": p.amenities
            })

        return result, 200

    # POST /places/
    @api.expect(place_model)
    def post(self):
        data = request.json

        # validate owner exists
        owner = facade.get_user(data["owner_id"])
        if not owner:
            return {"error": "Owner not found"}, 404

        place = facade.create_place(data)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": place.amenities
        }, 201


@api.route('/<string:place_id>')
class PlaceResource(Resource):

    # GET /places/<id>
    def get(self, place_id):
        p = facade.get_place(place_id)

        if not p:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(p.owner_id)

        return {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": p.price,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "owner": {
                "id": owner.id if owner else None,
                "first_name": owner.first_name if owner else None,
                "last_name": owner.last_name if owner else None
            },
            "amenities": p.amenities,
            "reviews": p.reviews if hasattr(p, "reviews") else []
        }, 200

    # PUT /places/<id>
    @api.expect(place_model)
    def put(self, place_id):
        data = request.json

        place = facade.update_place(place_id, data)

        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": place.amenities
        }, 200