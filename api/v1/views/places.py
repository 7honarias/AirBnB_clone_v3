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


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def route_place(city_id=None):
    """ City route dacec983-cec4-4f68-bd7f-af9068a305f5"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    new_list = []
    for place in (city.places):
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def route_place_id(place_id=None):
    """ Places route """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def route_delete_place(place_id=None):
    """ Places route delete """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def route_post_place(city_id=None):
    """Places city route """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    obj = request.get_json()
    if obj is None:
        abort(400, "Not a JSON")
    if 'user_id' not in obj:
        abort(400, "Missing user_id")
    user = storage.get(User, obj['user_id'])
    if user is None:
        abort(404)
    if 'name' not in obj:
        abort(400, "Missing name")
    obj['city_id'] = city_id
    place = Place(**obj)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id=None):
    """ States PUT route """
    ignore_keys = ['id', 'created_at', 'updated_at', 'city_id', 'user_id']
    obj = request.get_json()
    if obj is None:
        return make_response("Not a JSON", 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for k, v in obj.items():
        if k not in ignore_keys:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
