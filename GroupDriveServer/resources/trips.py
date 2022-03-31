from flask_restful import Resource
from flask import Response, request
from database.models import Trip


class TripApi(Resource):

    def get(self, id):
        trip = Trip.objects().get(id=id)
        return Response(trip, mimetype='application/json', status=200)

    def put(self, id):
        body = request.get_json(force=True)
        trip = Trip.objects().get(id=id)
        trip.update(**body)
        trip.save()
        return Response(status=200)

    def delete(self, id):
        trip = Trip.objects().get(id=id)
        trip.delete()
        return Response(status=200)


class TripsApi(Resource):

    def get(self):
        trips = Trip.objects().to_json()
        return Response(trips, mimetype='application/json', status=200)

    def post(self):
        body = request.get_json(force=True)
        trip = Trip(**body)
        trip.save()
        return Response(mimetype='application/json', status=200)
