#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, Place
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def places_by_city(city_id):
    """Return all places in a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return(jsonify([x.to_dict() for x in city.places]))


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def places_get_all():
    """Return all place dictionaries"""
    return (jsonify([x.to_dict() for x in storage.all("Place").values()]))


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def places_get(place_id):
    """Return attribute dictionary for a particular place"""
    get_places = storage.get("Place", place_id)
    if get_places is None:
        abort(404)
    return (jsonify(get_places.to_dict()))


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def places_delete(place_id):
    """Delete a place from storage"""
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    storage.save()
    return (jsonify({}))


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def places_post(city_id):
    """Add a place to storage with given dictionary"""
    try:
        obj = request.get_json()

        if storage.get("City", city_id) is None:
            abort(404)
        if "user_id" not in obj:
            return "Missing user_id", 400
        if storage.get("User", obj["user_id"]) is None:
            abort(404)
        if "name" not in obj:
            return "Missing name", 400

        obj["city_id"] = city_id
        obj = Place(**obj)
        obj.save()
        return jsonify(obj.to_dict()), 201

    except BadRequest:
        return "Not a JSON", 400


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def places_put(place_id):
    """Update a place in storage"""
    try:
        put_place = storage.get("Place", place_id)
        if put_place is None:
            abort(404)

        obj = request.get_json()

        for key, value in obj.items():
            if key in ["id", "created_at", "updated_at", "city_id", "user_id"]:
                continue
            else:
                setattr(put_place, key, value)
        put_place.save()
        return (jsonify(put_place.to_dict())), 200

    except BadRequest:
        return "Not a JSON", 400
