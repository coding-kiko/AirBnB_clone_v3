#!/usr/bin/python3
""" app.py """

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def remove_sesh(self):
    '''remove the current SQLAlchemy Session after request'''
    storage.close()


@app.errorhandler(404)
def page_not_found():
    '''404 page not found handler'''
    err = {"error": "Not found"}
    return (jsonify(**err))

if __name__ == "__main__":
    h = getenv('HBNB_API_HOST')
    p = getenv('HBNB_API_PORT')
    if not h:
        h = '0.0.0.0'
    if not p:
        p = 5000
    app.run(host=h, port=p, threaded=True)
