#!/usr/bin/python3
""" handles restful api actions """

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all State objects"""
    state_list = []
    if (state_id):
        for state in storage.all("State").values():
            if state.id == state_id:
                state_list.append(state)
        if len(state_list == 0):
            abort(404)
    else:
        for state in storage.all("State").values():
            state_list.append(state.to_dict())
    return (jsonify(state_list))


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    """ Deletes an state obj based on its id """
    f = False
    d = {}
    for state in storage.all("State").values():
        if state.id == state_id:
            state.delete()
            f = True
    if f:
        return (jsonify(**d))
    abort(404)
'''
@app_views.route('/states/<string:state_id>', methods=['POST'], strict_slashes=False)
def create_state(state_id):
    """ creates an state obj based on its id """


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates an state obj based on its id """
'''
