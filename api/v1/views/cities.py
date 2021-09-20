#!/usr/bin/python3
""" city views """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves all cities of a state"""
    if not storage.get("State", state_id):
        abort(404)
    cities_list = []
    for city in storage.all("City").values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return (jsonify(cities_list))

@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves city by id"""
    city = storage.get("City", city_id)
    if city:
        return (jsonify(city.to_dict()))
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_id(city_id):
    """ Deletes an city by id """
    
    city = storage.get("City", city_id)
    if city:
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ creates an city obj based on state id """

    new_city = request.get_json()

    if not storage.get("State", state_id):
        abort(404)
    if not new_city:
        abort(400, 'Not a JSON')
    if "name" not in new_city:
        abort(400, 'Missing name')

    new_city["state_id"] = state_id
    obj = City(**new_city)
    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates an city obj based on its id """

    ignored_keys = ["id", "created_at", "updated_at", "state_id"]
    new_city = request.get_json()

    if not new_city:
        abort(400, 'Not a JSON')

    for key in ignored_keys:
        if key in new_city:
            del new_city[key]

    city = storage.get("City", city_id)
    if city:
        for key, value in new_city.items():
            setattr(city, key, value)

        storage.save()
        return (jsonify(city.to_dict()), 200)

    abort(404)
