from flask_restful import Resource
from flask import Response, request
from bson.json_util import dumps
from database.models import Trip, User, UserLiveGPSCoordinates
from mongoengine.errors import DoesNotExist
from resources.errors import (
    TripNotExistsError,
    UserNotExistsError,
    UnauthorizedError,
    InternalServerError,
)
from datetime import datetime as dt
import uuid
class TripApi(Resource):
    def get(self, tripId):
        try:
            trip = Trip.objects().get(_id=tripId)
            # Updating the field isTripToday
            trip.update_trip()
            return Response(trip.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            raise TripNotExistsError

    def put(self, tripId):
        user = request.headers.get("username")
        body = request.get_json(force=True)
        try:
            trip = Trip.objects().get(_id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        # Checking permissions - user must be creator
        if trip.creator != user:
            raise UnauthorizedError
        trip.update(**body)
        trip.update_trip()
        return Response(status=200)

    def delete(self, tripId):
        try:
            trip = Trip.objects().get(_id=tripId)

        except DoesNotExist:
            raise TripNotExistsError

        user = request.headers.get("username")
        if (user != trip.creator):
            return UnauthorizedError

        # Deleting all existing coordinates for this trip from the database.
        try:
            coordinates = UserLiveGPSCoordinates.objects().filter(tripID=tripId)
            for c in coordinates:
                c.delete()
        except DoesNotExist:
            pass

        trip.delete()
        return Response(status=200)


class TripsApi(Resource):
    def get(self):
        trips = Trip.objects(date__gte=dt.today).order_by('date')
        tripsList = []
        creator_filter = request.headers.get("creator")
            
        for trip in trips:
            if creator_filter != None:
                print("creatore_filter header: ",creator_filter)
                if trip.creator != creator_filter:
                    continue
            trip.update_trip()
            trip_dict = trip.to_mongo().to_dict()
            trip_dict['date'] = trip.date.isoformat()
            tripsList.append(trip_dict)
        trips_json=dumps(tripsList)
        return Response(trips_json, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json(force=True)
        trip = Trip(**body)
        if trip.date == "":
            trip.date = dt.today()
        trip.participants.append(trip.creator)
        trip.save()
        return Response(mimetype="application/json", status=200)


class GetCoordinatesAPI(Resource):
    def get(self, tripId):
        try:
            trip = Trip.objects().get(_id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        coordinates = trip.get_participants_coordinates()
        return Response(coordinates, mimetype="application/json", status=200)


class UpdateCoordinatesAPI(Resource):
    def post(self, tripId):
        user = request.headers.get("username")
        try:
            trip = Trip.objects().get(_id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        body = request.get_json(force=True)
        body["user"] = user
        body["tripID"] = tripId
        newCoordinates = UserLiveGPSCoordinates(**body)
        if newCoordinates.is_valid() is not True:
            raise InternalServerError

        # if user allready has coordinates in the database update it
        try:
            userCoordinate = UserLiveGPSCoordinates.objects().get(
                user=user, tripID=tripId
            )
        except DoesNotExist:
            newCoordinates._id=str(uuid.uuid4())
            newCoordinates.save()
            return Response(status=200)

        userCoordinate.update(
            longitude=newCoordinates.longitude, latitude=newCoordinates.latitude
        )
        userCoordinate.save()
        return Response(status=200)


class JoinTripApi(Resource):
    def post(self, tripId):
        user = request.headers.get("username")
        try:
            trip = Trip.objects().get(_id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        
        trip.add_user(user)
        return Response(status=200)
