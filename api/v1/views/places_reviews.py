#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, Review
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def reviews_by_place(place_id):
    """Return all reviews in a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return(jsonify([x.to_dict() for x in place.reviews]))


@app_views.route("/reviews", methods=["GET"], strict_slashes=False)
def reviews_get_all():
    """Return all review dictionaries"""
    return (jsonify([x.to_dict() for x in storage.all("Review").values()]))


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def reviews_get(review_id):
    """Return attribute dictionary for a particular review"""
    get_reviews = storage.get("Review", review_id)
    if get_reviews is None:
        abort(404)
    return (jsonify(get_reviews.to_dict()))


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def reviews_delete(review_id):
    """Delete a review from storage"""
    reviews = storage.get("Review", review_id)
    if reviews is None:
        abort(404)
    storage.delete(reviews)
    storage.save()
    return (jsonify({}))


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def reviews_post(place_id):
    """Add a review to storage with given dictionary"""
    try:
        obj = request.get_json()

        if storage.get("Place", place_id) is None:
            abort(404)
        if "user_id" not in obj:
            return "Missing user_id", 400
        if storage.get("User", obj["user_id"]) is None:
            abort(404)
        if "text" not in obj:
            return "Missing text", 400

        obj["place_id"] = place_id
        obj = Review(**obj)
        obj.save()
        return jsonify(obj.to_dict()), 201

    except BadRequest:
        return "Not a JSON", 400


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def reviews_put(review_id):
    """Update a review in storage"""
    try:
        put_review = storage.get("Review", review_id)
        if put_review is None:
            abort(404)

        obj = request.get_json()

        for key, value in obj.items():
            if key in ["id", "created_at", "updated_at", "place_id", "user_id"]:
                continue
            else:
                setattr(put_review, key, value)
        put_review.save()
        return (jsonify(put_review.to_dict())), 200

    except BadRequest:
        return "Not a JSON", 400
