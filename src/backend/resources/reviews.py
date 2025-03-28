from flask import request
from flask_restful import Resource
from models import db, Review

class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return [{'id': r.id, 'game_title': r.game_title, 'review_text': r.review_text, 'rating': r.rating} for r in reviews], 200

    def post(self):
        json_data = request.get_json(force=True)
        new_review = Review(game_title=json_data['game_title'], review_text=json_data['review_text'], rating=json_data['rating'])
        db.session.add(new_review)
        db.session.commit()
        return {'message': 'Review created', 'id': new_review.id}, 201

    def put(self, review_id):
        json_data = request.get_json(force=True)
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        review.game_title = json_data['game_title']
        review.review_text = json_data['review_text']
        review.rating = json_data['rating']
        db.session.commit()
        return {'message': 'Review updated'}, 200

    def delete(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        db.session.delete(review)
        db.session.commit()
        return {'message': 'Review deleted'}, 204