#!/usr/bin/python3
''' Index '''

from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def status():
    '''returns request status'''
    jsn = {"status": "OK"}
    return (jsonify(**jsn))
