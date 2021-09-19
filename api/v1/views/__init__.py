#!/usr/bin/python3
""" Init """

from flask import Flask, Blueprint

app = Flask(__name__)
app_views = Blueprint("app_views", __name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
