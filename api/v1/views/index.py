#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    d = {"status": "OK"}
    return (jsonify(d))
