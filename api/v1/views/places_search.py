#!/usr/bin/python3
"""
    Create restful API for project HBNB
"""
from api.v1.views import app_views
from models import storage, State
from flask import jsonify, abort, request
from json import dumps
from werkzeug.exceptions import BadRequest


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """Return all palces matching search criteria"""
    criteria = request.get_json(silent=True)
    if criteria is None:
        return (jsonify([x.to_dict() for x in storage.all("Place").values()]))
    states = storage.all("State")
    try:
        states = [x for x in criteria["states"]]
    except KeyError:
        states = []
    cities = storage.all("City")
    try:
        cities = [x for x in criteria["cities"]]
    except KeyError:
        cities = []
    amenities = storage.all("Amenity")
    try:
        amenities = [x for x in criteria["amenities"]]
    except KeyError:
        amenities = []
    places = list(storage.all("Place").values())
    if len(states) == 0 and len(cities) == 0 and len(amenities) == 0:
        return (jsonify([x.to_dict() for x in places]))

    placematch = []
    for place in places:
        if len(cities) != 0 and place.city_id not in cities:
            continue
        if len(states) != 0 and\
           storage.get("City", place.city_id).state_id not in states:
            continue
        noamenity = 0
        if len(amenities) != 0:
            placeamenities = place.amenities
            if len(placeamenities) == 0:
                noamenity = 1
            for amenity in placeamenities:
                if amenity.id not in amenities:
                    noamenity = 1
                    break
        if noamenity == 1:
            continue

        placematch.append(place)

    retdicts = [x.to_dict() for x in placematch]
    for place in retdicts:
        try:
            amenitylist = place["amenities"]
            finallist = []
            for amenity in range(len(amenitylist)):
                finallist.append(amenitylist[amenity].to_dict())
            place["amenities"] = finallist
        except KeyError:
            pass
    return (jsonify(retdicts))
