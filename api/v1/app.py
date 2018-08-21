#!/usr/bin/python3
"""
    Create a restful API using flask
"""
if __name__ == "__main__":

    from models import storage
    from api.v1.views import app_views
    import flask

    app = flask.Flask(__name__)
    app.register_blueprint(app_views, url_prefix="/api/v1")

    @app.teardown_appcontext
    def flask_teardown(error):
        storage.close()

    app.run(threaded=True, host="0.0.0.0", port=5000)
