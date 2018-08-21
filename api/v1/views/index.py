#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route("/status")
def status():
    d = {"status": "OK"}
    return (jsonify(d))

@app_views.route("/stats")
def count_up():
    d = {}

    d["amenities"] = storage.count("Amenity")
    d["cities"] = storage.count("City")
    d["places"] = storage.count("Place")
    d["reviews"] = storage.count("Review")
    d["states"] = storage.count("State")
    d["users"] = storage.count("User")

    return (jsonify(d))
