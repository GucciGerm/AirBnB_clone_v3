#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, Amenity
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities_get_all():
    """Return all amenity dictionaries"""
    return (jsonify([x.to_dict() for x in storage.all("Amenity").values()]))


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def amenities_get(amenity_id):
    """Return attribute dictionary for a particular amenity"""
    get_amenities = storage.get("Amenity", amenity_id)
    if get_amenities is None:
        abort(404)
    return (jsonify(get_amenities.to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenities_delete(amenity_id):
    """Delete a amenity from storage"""
    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return (jsonify({}))


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenities_post():
    """Add a amenity to storage with given dictionary"""
    try:
        obj = request.get_json()

        if "name" not in obj:
            return "Missing name", 400

        obj = Amenity(**obj)
        obj.save()
        return jsonify(obj.to_dict()), 201

    except BadRequest:
        return "Not a JSON", 400


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenities_put(amenity_id):
    """Update a amenity in storage"""
    try:
        put_amenity = storage.get("Amenity", amenity_id)
        if put_amenity is None:
            abort(404)

        obj = request.get_json()

        for key, value in obj.items():
            if key == "id" or key == "created_at" or key == "updated_at":
                continue
            else:
                setattr(put_amenity, key, value)
        put_amenity.save()
        return (jsonify(put_amenity.to_dict())), 200

    except BadRequest:
        return "Not a JSON", 400
