from flask_restful import Resource
from flask import Response
from database.models import Trip, User, UserInTrip
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

        userInTrip = UserInTrip()
        userInTrip.user = user
        userInTrip.trip = trip
        userInTrip.save()
        return Response(userInTrip.get('_id'),
                        mimetype='application/json', status=200)
