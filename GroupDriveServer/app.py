from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from resources.routes import initialize_routes
    

app = Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost"

mongo = PyMongo(app)
db = mongo.db

api = Api(app)

initialize_routes(api)