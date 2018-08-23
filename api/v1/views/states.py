#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, State
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states_get_all():
    """Return all state dictionaries"""
    return (jsonify([x.to_dict() for x in storage.all("State").values()]))


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states_get(state_id):
    """Return attribute dictionary for a particular state"""
    get_states = storage.get("State", state_id)
    if get_states is None:
        abort(404)
    return (jsonify(get_states.to_dict()))


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def states_delete(state_id):
    """Delete a state from storage"""
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return (jsonify({}))


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def states_post():
    """Add a state to storage with given dictionary"""
    try:
        obj = request.get_json()

        if "name" not in obj:
            return "Missing name", 400

        obj = State(**obj)
        obj.save()
        return jsonify(obj.to_dict()), 201

    except BadRequest:
        return "Not a JSON", 400


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def states_put(state_id):
    """Update a state in storage"""
    try:
        put_state = storage.get("State", state_id)
        if put_state is None:
            abort(404)

        obj = request.get_json()

        for key, value in obj.items():
            if key == "id" or key == "created_at" or key == "updated_at":
                continue
            else:
                setattr(put_state, key, value)
        put_state.save()
        return (jsonify(put_state.to_dict())), 200

    except BadRequest:
        return "Not a JSON", 400
