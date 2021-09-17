#!/usr/bin/python3
""" handles restful api actions """

from flask import Flask, jsonify, abort
from models.state import State
from api.v1.views import app_views
from models import storage

@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    print("llega -----------------")
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
    return (jsonify(**state_list))


#@app_views.route('/states/<state_id>', methods=['DELETE'])
#def delete_state_id(state_id):
