#!/usr/bin/python3
''' Index '''

from api.v1.views import app_views, app
from models.amenity import Amenity
from models.city import City
from flask import jsonify
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    '''returns request status'''
    jsn = {
        "status": "OK"
        }
    return (jsonify(**jsn))


@app_views.route('/stats', strict_slashes=False)
def n_of_inst():
    '''retrieves n of each instance'''
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    for cls_str, cls in classes.items():
        classes[cls_str] = storage.count(cls)
    return (jsonify(**classes))
