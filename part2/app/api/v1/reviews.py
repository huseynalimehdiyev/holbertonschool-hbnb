from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')


review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Float(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})


@api.route('/')
class ReviewList(Resource):

    # GET /reviews/
    def get(self):
        reviews = facade.get_all_reviews()

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id,
                "place_id": r.place_id
            }
            for r in reviews
        ], 200

    # POST /reviews/
    @api.expect(review_model)
    def post(self):
        data = request.json

        review = facade.create_review(data)

        if not review:
            return {"error": "User or Place not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    # GET
    def get(self, review_id):
        r = facade.get_review(review_id)

        if not r:
            return {"error": "Review not found"}, 404

        return {
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "place_id": r.place_id
        }, 200

    # PUT
    @api.expect(review_model)
    def put(self, review_id):
        data = request.json
        r = facade.update_review(review_id, data)

        if not r:
            return {"error": "Review not found"}, 404

        return {
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "place_id": r.place_id
        }, 200

    def delete(self, review_id):
        deleted = facade.delete_review(review_id)

        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted"}, 200