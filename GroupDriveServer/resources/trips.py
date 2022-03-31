from flask_restful import Resource
from flask import Response
from database.models import User, Trip, UserLiveGPSCoordinate 

class onShowTrips(Resource):
    def post(self):
        trips = Trip.objects().to_json()
        return Response(trips, mimetype="application/json", status=200)

class onJoinTrip(Resource):
    def post(self, trip_id, user_id):
        print("onJoinTrip")

class onEditTrip(Resource):
    def post(self):
        print("onEditTrip")
