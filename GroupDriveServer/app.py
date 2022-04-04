from flask import Flask
from flask_restful import Api
from resources.routes import initialize_routes
from database.db import initialize_db
from flask_jwt_extended import JWTManager


def create_app(configFileName):
    app = Flask("__name__")

    app.config.from_pyfile(configFileName)
    app.debug = True

    api = Api(app)
    jwt = JWTManager(app)

    # Init our database.

    initialize_db(app)

    # Define the routes of the server.

    initialize_routes(api)

    return app
