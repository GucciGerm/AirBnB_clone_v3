#!/usr/bin/python3
"""
    Create a restful API using flask
"""
if __name__ == "__main__":

    from models import storage
    from api.v1.views import app_views
    from flask import jsonify
    import flask

    app = flask.Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_blueprint(app_views, url_prefix="/api/v1")

    @app.teardown_appcontext
    def flask_teardown(error):
        storage.close()

    @app.errorhandler(404)
    def page_not_found(exception):
        d = {"error": "Not found"}
        return (jsonify(d))

    app.run(threaded=True, host="0.0.0.0", port=5000)
