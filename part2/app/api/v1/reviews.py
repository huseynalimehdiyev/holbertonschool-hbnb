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

    def get(self):
        reviews = facade.get_all_reviews()
        return [r.__dict__ for r in reviews], 200

    @api.expect(review_model)
    def post(self):
        data = request.json

        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not review:
            return {"error": "User or Place not found"}, 404

        return review.__dict__, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.__dict__, 200

    @api.expect(review_model)
    def put(self, review_id):
        data = request.json
        try:
            review = facade.update_review(review_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not review:
            return {"error": "Review not found"}, 404

        return review.__dict__, 200

    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Deleted"}, 200