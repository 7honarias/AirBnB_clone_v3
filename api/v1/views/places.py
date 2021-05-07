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
    
    cities = storage.get(City, 'dacec983-cec4-4f68-bd7f-af9068a305f5')
    if cities is None:
        abort(404)
    if cities is not None:
        new_list = []
        for city in (cities.places):
            new_list.append(city.to_dict())
    return jsonify(new_list)
    





