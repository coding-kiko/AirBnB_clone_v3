#!/usr/bin/python3
""" handles restful api actions """

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """Gets all places from given city"""
    city = storage.get("City", city_id)
    if city:
        places_list = []
        for place in storage.all("Place").values():
            if place.city_id == city_id:
                places_list.append(place.to_dict())
        return (jsonify(places_list))
    abort(404)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a place by id"""
    place = storage.get("Place", place_id)
    if place:
        return (jsonify(place.to_dict()))
    abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    """ Deletes an place obj based on its id """

    for place in storage.all("Place").values():
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return (jsonify({}), 200)

    abort(404)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ creates an place obj based on its id """

    new_place = request.get_json()

    city = storage.get("City", city_id)
    if city:
        if not new_place:
            abort(400, 'Not a JSON')
        if "user_id" not in new_place:
            abort(400, "Missing user_id")
        if not storage.get("User", new_place["user_id"]):
            abort(404)
        if "name" not in new_place:
            abort(400, 'Missing name')

        new_place["city_id"] = city_id
        obj = Place(**new_place)
        storage.new(obj)
        storage.save()

        return (jsonify(obj.to_dict()), 201)
    abort(404)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ updates an place obj based on its id """

    ignored_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
    new_place = request.get_json()

    if not new_place:
        abort(400, 'Not a JSON')

    for key in ignored_keys:
        if key in new_place:
            del new_place[key]

    place = storage.get("Place", place_id)
    if place:
        for key, value in new_place.items():
            setattr(place, key, value)

        storage.save()
        return (jsonify(place.to_dict()), 200)

    abort(404)
