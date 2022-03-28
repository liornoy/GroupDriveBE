from flask import Flask

from database.db import initialize_db
from flask_restful import Api


app = Flask(__name__)
#app.config.from_envvar('ENV_FILE_LOCATION')

from resources.routes import initialize_routes

api = Api(app)

initialize_db(app)
initialize_routes(api)