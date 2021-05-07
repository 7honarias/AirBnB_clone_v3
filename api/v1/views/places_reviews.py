#!/usr/bin/python3
""" user view module """
from models import storage
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from flask import Flask, jsonify, abort, request
from flask import make_response
"""3ebfaf23-cede-4cf0-964d-8afc17b11d02"""


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def route_users(place_id=None):
    """ place route """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place is not None:
        new_list = []
        for review in (place.reviews):
            new_list.append(review.to_dict())
        return jsonify(new_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def route_review(review_id=None):
    """f694d9ce-2e60-44b1-95b0-2f4ebe2ed52d"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def route_delete(review_id=None):
    """f694d9ce-2e60-44b1-95b0-2f4ebe2ed52d"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def route_post(place_id):
    """State POST Route 32c11d3d-99a1-4406-ab41-7b6ccb7dd760 user
     place 3ebfaf23-cede-4cf0-964d-8afc17b11d02
    """
    try:
        obj = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'text' not in obj:
        abort(400, 'Missing text')
    if 'user_id' not in obj:
        abort(400, 'Missing user_id')
    user = storage.get(User, obj['user_id'])
    if user is None:
        abort(404)
    amenitie = Review(**obj)
    setattr(amenitie, "place_id", place_id)

    storage.new(amenitie)
    storage.save()
    return make_response(jsonify(amenitie.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def reviews_put(review_id=None):
    """ States PUT route """
    try:
        obj = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for k, v in obj.items():
        if k not in ['id', 'created_at', 'updated_at', 'place_id', 'user_id']:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
