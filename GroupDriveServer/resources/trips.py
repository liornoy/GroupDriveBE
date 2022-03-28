from flask_restful import Resource

class onShowTrips(Resource):
    def post(self):
        print("onShowTrips")

class onJoinTrip(Resource):
    def post(self):
        print("onJoinTrip")

class onEditTrip(Resource):
    def post(self):
        print("onEditTrip")