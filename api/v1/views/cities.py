#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, City
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def cities_by_state(state_id):
    """Return all cities in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return(jsonify([x.to_dict() for x in state.cities]))


@app_views.route("/cities", methods=["GET"], strict_slashes=False)
def cities_get_all():
    """Return all city dictionaries"""
    return (jsonify([x.to_dict() for x in storage.all("City").values()]))


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def cities_get(city_id):
    """Return attribute dictionary for a particular city"""
    get_cities = storage.get("City", city_id)
    if get_cities is None:
        abort(404)
    return (jsonify(get_cities.to_dict()))


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def cities_delete(city_id):
    """Delete a city from storage"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    storage.save()
    return (jsonify({}))


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def cities_post(state_id):
    """Add a city to storage with given dictionary"""
    obj = request.get_json(silent=True)
    if obj is None:
        return "Not a JSON", 400

    if storage.get("State", state_id) is None:
        abort(404)
    if "name" not in obj:
        return "Missing name", 400

    obj["state_id"] = state_id
    obj = City(**obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def cities_put(city_id):
    """Update a city in storage"""
    put_city = storage.get("City", city_id)
    if put_city is None:
        abort(404)

    obj = request.get_json(silent=True)
    if obj is None:
        return "Not a JSON", 400

    for key, value in obj.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(put_city, key, value)
    put_city.save()
    return (jsonify(put_city.to_dict())), 200
