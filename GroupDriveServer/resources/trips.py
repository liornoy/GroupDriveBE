from flask_restful import Resource
from flask import Response, request
from database.models import Trip
from mongoengine.errors import DoesNotExist
from resources.errors import TripNotExistsError


class TripApi(Resource):

    def get(self, trip_id):
        try:
            trip = Trip.objects().get(id=trip_id)
            # Updating the field isTripToday
            trip.updateTrip()
            return Response(trip.to_json(), mimetype = 'application/json', status=200)
        except DoesNotExist:
            raise TripNotExistsError
        
        

    def put(self, trip_id):
        try:
            body = request.get_json(force=True)
            trip = Trip.objects().get(id=trip_id)
            trip.update(**body)
            trip.save()
            return Response(status=200) 
        except DoesNotExist:
            raise TripNotExistsError
        

    def delete(self, trip_id):
        try:
            trip = Trip.objects().get(id=trip_id)
            trip.delete()
            return Response(status=200)
        except DoesNotExist:
            raise TripNotExistsError



class TripsApi(Resource):

    def get(self):
        trips = Trip.objects()
        tripsList = list(trips)
        for trip in tripsList:
            trip.updateTrip()
        return Response(trips.to_json(), mimetype='application/json', status=200)

    def post(self):
        body = request.get_json(force=True)
        trip = Trip(**body)
        trip.save()
        return Response(mimetype='application/json', status=200)
