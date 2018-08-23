#!/usr/bin/python3
"""
    Create restful API for hbnb project
"""


from flask import Blueprint
app_views = Blueprint("app_views", __name__)

if True:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *
