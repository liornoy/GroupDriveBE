from flask import Flask
from flask_restful import Api
from resources.routes import initialize_routes
from database.db import initialize_db

app = Flask('__name__')

app.config['MONGO_URI'] = 'mongodb+srv://localhost/groupdrive'

app.debug = True

api = Api(app)

# Init our database.

initialize_db(app)

# Define the routes of the server.

initialize_routes(api)

app.run(debug=True)
