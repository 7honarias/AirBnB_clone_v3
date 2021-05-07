#!/usr/bin/python3
""" amenitie view module """
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask import make_response


@app_views.route('/amenities', strict_slashes=False)
@app_views.route('/amenities/<amenitie_id>', methods=['GET', 'DELETE'])
def route_amenitie(amenitie_id=None):
    """ Amenitie route """
    if amenitie_id is None:
        all_amenities = storage.all(Amenity)
        new_list = []
        for amenities in all_amenities.values():
            new_list.append(amenities.to_dict())
        return jsonify(new_list)
    amenitie = storage.get(Amenity, amenitie_id)
    # Return 404 if amenitie_id is not in storage
    if amenitie is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenitie.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenitie)
        storage.save()
        return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenitie_post():
    """Amenitie POST Route"""
    try:
        obj = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in obj:
        abort(400, 'Missing name')
    amenitie = Amenity(**obj)
    storage.new(amenitie)
    storage.save()
    return make_response(jsonify(amenitie.to_dict()), 201)


@app_views.route('/amenities/<amenitie_id>', methods=['PUT'])
def amenitie_put(amenitie_id=None):
    """Amenitie PUT route """
    try:
        obj = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    amenitie = storage.get(Amenity, amenitie_id)
    if amenitie is None:
        abort(404)
    for k, v in obj.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(amenitie, k, v)
    storage.save()
    return make_response(jsonify(amenitie.to_dict()), 200)
