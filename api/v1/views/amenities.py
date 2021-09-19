#!/usr/bin/python3
""" handles restful api actions """

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """Retrieves the list of all amenity objects"""
    if (amenity_id):
        for amenity in storage.all("amenity").values():
            if amenity.id == amenity_id:
                return (jsonify(amenity.to_dict()))
        abort(404)

    else:
        amenity_list = []
        for amenity in storage.all("amenity").values():
            amenity_list.append(amenity.to_dict())
        return (jsonify(amenity_list))


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_id(amenity_id):
    """ Deletes an amenity obj based on its id """
    
    for amenity in storage.all("amenity").values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return (jsonify({}), 200)

    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ creates an amenity obj based on its id """

    new_amenity = request.get_json()

    if not new_amenity:
        abort(400, 'Not a JSON')
    if "name" not in new_amenity:
        abort(400, 'Missing name')

    obj = Amenity(**new_amenity)
    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ updates an amenity obj based on its id """

    ignored_keys = ["id", "created_at", "updated_at"]
    new_amenity = request.get_json()

    if not new_amenity:
        abort(400, 'Not a JSON')

    for key in ignored_keys:
        if key in new_amenity:
            del new_amenity[key]

    amenity = storage.get("amenity", amenity_id)
    if amenity:
        for key, value in new_amenity.items():
            setattr(amenity, key, value)

        storage.save()
        return (jsonify(amenity.to_dict()), 200)

    abort(404)
