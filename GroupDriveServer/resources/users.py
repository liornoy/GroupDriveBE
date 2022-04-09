from flask_restful import Resource
from flask import Response, request
from .errors import UserNotExistsError
from mongoengine.errors import DoesNotExist
from database.models import User, UserLiveGPSCoordinates

# from database.preference_enum import EPreference

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
            user.save()

        return Response(status=200)

    def put(self):
        userGoogleId = request.headers.get("google-id")
        body = request.get_json(force=True)
        try:
            user = User.objects().get(googleID=userGoogleId)
        except DoesNotExist:
            raise UserNotExistsError

        user.update(**body)
        user.save()
        return Response(status=200)

    def delete(self):
        userGoogleId = request.headers.get("google-id")
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
