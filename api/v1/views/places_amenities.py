#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, Amenity
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def amenities_by_place(place_id):
    """Return all amenities in a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return(jsonify([x.to_dict() for x in place.amenities]))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Delete a amenity from a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenities = place.amenities
    if amenity not in amenities:
        abort(404)
    amenities.remove(amenity)
    place.amenities = amenities
    place.save()
    return (jsonify({}))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """Add an amenity to a place with given id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    amenities = place.amenities
    if amenity in amenities:
        return jsonify(amenity.to_dict())
    amenities.append(amenity)
    place.amenities = amenities
    place.save()
    return jsonify(amenity.to_dict()), 201
