from flask import Flask
from flask_restful import Api
from resources.routes import initialize_routes
from database.db import initialize_db
from flask_jwt_extended import JWTManager

app = Flask('__name__')

app.config.from_envvar('ENV_FILE_LOCATION')
app.debug = True

api = Api(app)
jwt = JWTManager(app)

# Init our database.

initialize_db(app)

# Define the routes of the server.

initialize_routes(api)

app.run(debug=True)
