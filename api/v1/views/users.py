#!/usr/bin/python3
""" handles restful api actions """

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """Retrieves the list of all user objects"""
    if (user_id):
        for user in storage.all("User").values():
            if user.id == user_id:
                return (jsonify(user.to_dict()))
        abort(404)

    else:
        user_list = []
        for user in storage.all("User").values():
            user_list.append(user.to_dict())
        return (jsonify(user_list))


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_id(user_id):
    """ Deletes an user obj based on its id """

    for user in storage.all("User").values():
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            return (jsonify({}), 200)

    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creates an user obj based on its id """

    new_user = request.get_json()

    if not new_user:
        abort(400, 'Not a JSON')
    if "email" not in new_user:
        abort(400, 'Missing email')
    if "password" not in new_user:
        abort(400, 'Missing password')

    obj = User(**new_user)
    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates an user obj based on its id """

    ignored_keys = ["id", "created_at", "updated_at", "email"]
    new_user = request.get_json()

    if not new_user:
        abort(400, 'Not a JSON')

    for key in ignored_keys:
        if key in new_user:
            del new_user[key]

    user = storage.get("User", user_id)
    if user:
        for key, value in new_user.items():
            setattr(user, key, value)

        storage.save()
        return (jsonify(user.to_dict()), 200)

    abort(404)
