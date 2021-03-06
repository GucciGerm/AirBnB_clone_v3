#!/usr/bin/python3
"""
    Create a restful API using flask
"""


from models import storage
from api.v1.views import app_views
from flask import jsonify, Flask
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def flask_teardown(error):
    """Teardown after flask app runs"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """404 page handler"""
    d = {"error": "Not found"}
    return (jsonify(d)), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", default=5000)), threaded=True)
