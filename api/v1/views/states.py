#!/usr/bin/python3
""" handles restful api actions """

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all State objects"""
    if (state_id):
        for state in storage.all("State").values():
            if state.id == state_id:
                return (jsonify(state.to_dict()))
        abort(404)

    else:
        state_list = []
        for state in storage.all("State").values():
            state_list.append(state.to_dict())
        return (jsonify(state_list))


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    """ Deletes an state obj based on its id """
    
    for state in storage.all("State").values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return (jsonify({}), 200)

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates an state obj based on its id """

    new_state = request.get_json()

    if not new_state:
        abort(400, 'Not a JSON')
    if "name" not in new_state:
        abort(400, 'Missing name')

    obj = State(**new_state)
    storage.new(obj)
    storage.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates an state obj based on its id """

    ignored_keys = ["id", "created_at", "updated_at"]
    new_state = request.get_json()

    if not new_state:
        abort(400, 'Not a JSON')

    for key in ignored_keys:
        if key in new_state:
            del new_state[key]

    state = storage.get("State", state_id)
    if state:
        for key, value in new_state.items():
            setattr(state, key, value)

        storage.save()
        return (jsonify(state.to_dict()), 200)

    abort(404)
