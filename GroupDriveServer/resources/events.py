from flask_restful import Resource
from flask import request, Response
from database.models import Trip, User, UserLiveGPSCoordinates
from mongoengine.errors import DoesNotExist
from resources.errors import TripNotExistsError, UserNotExistsError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.preference_enum import EPreference
import datetime

class JoinTripApi(Resource):
    @jwt_required
    def post(self,trip_id):
        user_id = get_jwt_identity()
        try:
            user = User.objects().get(googleID=user_id)
        except DoesNotExist:
            raise UserNotExistsError
        try:
            trip = Trip.objects().get(id=trip_id)
        except DoesNotExist:
            raise TripNotExistsError


        trip.participants.append(user)
        trip.save()
        return Response(status=200)



class LoginApi(Resource):

    def post(self):
        body = request.get_json(force=True)
        user = User(**body)
        
        try:
            User.objects().get(googleID = user.googleID)
            
        except DoesNotExist:
            preferences = {}
            for p in EPreference:
                preferences.update({p.name: 0})
            user.preferences = preferences
            user.save()

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.googleID), expires_delta=expires)
        return {'token': access_token}, 200