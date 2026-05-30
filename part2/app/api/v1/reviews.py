from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Float(required=True),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

# =========================
# /reviews/
# =========================
@api.route('/')
class ReviewList(Resource):

    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [r.__dict__ for r in reviews], 200

    @api.expect(review_model)
    @jwt_required()
    def post(self):
        """Create a new review (authenticated user only)"""
        data = request.json

        current_user_id = get_jwt_identity()

        # Ensure user_id in payload matches logged in user
        if data.get("user_id") != current_user_id:
            return {"error": "Cannot create review for another user"}, 403

        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not review:
            return {"error": "User or Place not found"}, 404

        return review.__dict__, 201


# =========================
# /reviews/<review_id>
# =========================
@api.route('/<string:review_id>')
class ReviewResource(Resource):

    def get(self, review_id):
        """Get a single review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.__dict__, 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review (only owner can update)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        current_user_id = get_jwt_identity()
        if review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.json
        try:
            updated = facade.update_review(review_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated.__dict__, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (only owner can delete)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        current_user_id = get_jwt_identity()
        if review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted"}, 200