from flask_restful import Resource
from flask import Response, request
from database.models import Trip, User, UserLiveGPSCoordinates
from mongoengine.errors import DoesNotExist
from resources.errors import (
    TripNotExistsError,
    UserNotExistsError,
    UnauthorizedError,
    InternalServerError,
)


class TripApi(Resource):
    def get(self, tripId):
        try:
            trip = Trip.objects().get(id=tripId)
            # Updating the field isTripToday
            trip.updateTrip()
            return Response(trip.to_json(), mimetype="application/json", status=200)
        except DoesNotExist:
            raise TripNotExistsError

    def put(self, tripId, userGoogleId):
        userGoogleId = request.headers.get("google-id")
        body = request.get_json(force=True)
        try:
            trip = Trip.objects().get(id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        # Checking permissions - user must be creator
        if trip.creatorGID != userGoogleId:
            raise UnauthorizedError
        trip.update(**body)
        trip.updateTrip()
        trip.save()
        return Response(status=200)

    def delete(self, tripId):
        try:
            trip = Trip.objects().get(id=tripId)

        except DoesNotExist:
            raise TripNotExistsError
        # Deleting all existing coordinates for this trip from the database.
        try:
            coordinates = UserLiveGPSCoordinates.objects().filter(trip=trip)
            for c in coordinates:
                c.delete()
        except DoesNotExist:
            pass

        trip.delete()
        return Response(status=200)


class TripsApi(Resource):
    def get(self):
        trips = Trip.objects()
        tripsList = list(trips)
        for trip in tripsList:
            trip.updateTrip()
        return Response(trips.to_json(), mimetype="application/json", status=200)

    def post(self):
        userGoogleId = request.headers.get("google-id")
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError
        body = request.get_json(force=True)
        trip = Trip(**body)
        trip.creator = userGoogleId
        trip.participants.append(userGoogleId)
        trip.save()
        return Response(mimetype="application/json", status=200)


class GetCoordinatesAPI(Resource):
    def post(self, tripId):
        userGoogleId = request.headers.get("google-id")
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError
        try:
            trip = Trip.objects().get(id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        coordinates = trip.getParticipantsCoordinates()
        return Response(coordinates, status=200)


class UpdateCoordinatesAPI(Resource):
    def post(self, tripId):
        userGoogleId = request.headers.get("google-id")
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError
        try:
            trip = Trip.objects().get(id=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        body = request.get_json(force=True)
        body["user"] = user.id
        body["trip"] = trip.id
        newCoordinates = UserLiveGPSCoordinates(**body)

        if newCoordinates.isValid() is not True:
            raise InternalServerError

        try:
            userCoordinate = UserLiveGPSCoordinates.objects().get(user=user, trip=trip)
        except DoesNotExist:
            newCoordinates.save()
            return Response(status=200)

        userCoordinate.update(
            longitude=newCoordinates.longitude, latitude=newCoordinates.latitude
        )
        userCoordinate.save()
        return Response(status=200)


class JoinTripApi(Resource):
    def post(self, tripId):
        userGoogleId = request.headers.get("google-id")
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError

        try:
            trip = Trip.objects().get(tripID=tripId)
        except DoesNotExist:
            raise TripNotExistsError

        trip.addUser(user.googleID)
        return Response(status=200)
