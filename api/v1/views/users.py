#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, User
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_get_all():
    """Return all user dictionaries"""
    return (jsonify([x.to_dict() for x in storage.all("User").values()]))


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def users_get(user_id):
    """Return attribute dictionary for a particular user"""
    get_users = storage.get("User", user_id)
    if get_users is None:
        abort(404)
    return (jsonify(get_users.to_dict()))


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def users_delete(user_id):
    """Delete a user from storage"""
    users = storage.get("User", user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return (jsonify({}))


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def users_post():
    """Add a user to storage with given dictionary"""
    obj = request.get_json(silent=True)
    if obj is None:
        return "Not a JSON", 400

    if "email" not in obj:
        return "Missing email", 400
    if "password" not in obj:
        return "Missing password", 400

    obj = User(**obj)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def users_put(user_id):
    """Update a user in storage"""
    put_user = storage.get("User", user_id)
    if put_user is None:
        abort(404)

    obj = request.get_json(silent=True)
    if obj is None:
        return "Not a JSON", 400

    for key, value in obj.items():
        if key in ["id", "created_at", "updated_at", "email"]:
            continue
        else:
            setattr(put_user, key, value)
    put_user.save()
    return (jsonify(put_user.to_dict())), 200
