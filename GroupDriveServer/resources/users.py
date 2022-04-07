from flask_restful import Resource
from flask import Response, request
from .errors import UserNotExistsError
from mongoengine.errors import DoesNotExist
from database.models import User, UserLiveGPSCoordinates
from database.preference_enum import EPreference
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import datetime


class UserApi(Resource):
    def get(self, userId):
        user = User.objects().get(id=userId)
        return Response(user, mimetype="application/json", status=200)


class UsersApi(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json(force=True)
        user = User(**body)

        try:
            User.objects().get(googleID=user.googleID)

        except DoesNotExist:
            preferences = {}
            for p in EPreference:
                preferences.update({p.name: 0})
            user.preferences = preferences
            user.save()

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.googleID), expires_delta=expires
            )
        return {"token": access_token}, 200

    @jwt_required()
    def put(self):
        userGoogleId = get_jwt_identity()
        body = request.get_json(force=True)
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError

        user.update(**body)
        user.save()
        return Response(status=200)

    @jwt_required()
    def delete(self):
        userGoogleId = get_jwt_identity()
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError

        # Deleting all existing coordinates for this trip user the database.
        try:
            coordinates = UserLiveGPSCoordinates.objects().filter(user=user)
            for c in coordinates:
                c.delete()
        except DoesNotExist:
            pass

        user.delete()
        return Response(status=200)
