#!/usr/bin/python3
""" review views """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves all reviews of a place"""
    if not storage.get("Place", place_id):
        abort(404)
    reviews_list = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return (jsonify(reviews_list))


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves review by id"""
    review = storage.get("Review", review_id)
    if review:
        return (jsonify(review.to_dict()))
    abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_id(review_id):
    """ Deletes an review by id """

    review = storage.get("Review", review_id)
    if review:
        storage.delete(review)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ creates an review obj based on place id """

    new_review = request.get_json()

    if not storage.get("Place", place_id):
        abort(404)
    if not new_review:
        abort(400, 'Not a JSON')
    if "user_id" not in new_review:
        abort(400, 'Missing user_id')
    if not storage.get("User", new_review["user_id"]):
        abort(404)
    if "text" not in new_review:
        abort(400, "Missing text")

    new_review["place_id"] = place_id
    obj = Review(**new_review)
    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ updates an review obj based on its id """

    ignored_keys = ["id", "created_at", "updated_at", "place_id", "user_id"]
    new_review = request.get_json()

    if not new_review:
        abort(400, 'Not a JSON')

    for key in ignored_keys:
        if key in new_review:
            del new_review[key]

    review = storage.get("Review", review_id)
    if review:
        for key, value in new_review.items():
            setattr(review, key, value)

        storage.save()
        return (jsonify(review.to_dict()), 200)

    abort(404)
