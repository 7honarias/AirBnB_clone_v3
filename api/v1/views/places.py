#!/usr/bin/python3
""" State view module """
from models.amenity import Amenity
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask import make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def route_place(city_id=None):
    """ City route dacec983-cec4-4f68-bd7f-af9068a305f5"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    if cities is not None:
        new_list = []
        for city in (cities.places):
            new_list.append(city.to_dict())
    return jsonify(new_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def route_place_id(place_id=None):
    """ Places route """
    review = storage.get(Place, place_id)
    if review is None:
        abort(404)
    return(review.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def route_delete_place(place_id=None):
    """ Places route delete """
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def route_post_place(city_id):
    """Places city route """
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    if 'name' not in obj:
        abort(400, 'Missing name')
    if 'user_id' not in obj:
        abort(400, 'Missing user_id')
    city = storage.get(City, obj['city_id'])
    if user is None:
        abort(404)
    place = Place(**obj)
    setattr(place, "city_id", city_id)

    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def places_put(review_id=None):
    """ States PUT route """
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for k, v in obj.items():
        if k not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
