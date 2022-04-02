from flask_restful import Resource
from flask import Response
from database.models import Trip, User
from mongoengine.errors import DoesNotExist
from resources.errors import UserNotExistsError, TripNotExistsError


class JoinTripEvent(Resource):

    def post(self, user_id, trip_id):
        try:
            user = User.objects().get(id=user_id)
        except DoesNotExist:
            raise UserNotExistsError

        try:
            trip = Trip.objects().get(id=trip_id)
        except DoesNotExist:
            raise TripNotExistsError

        trip.participants.append(user)
        trip.save()
        return Response(status=200)
