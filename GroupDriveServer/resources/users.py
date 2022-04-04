from flask_restful import Resource
from flask import Response, request
from .errors import UserNotExistsError
from mongoengine.errors import DoesNotExist
from database.models import User


class UserApi(Resource):

    def get(self, user_id):
        user = User.objects().get(id=user_id)
        return Response(user, mimetype='application/json', status=200)

    def put(self, user_id):
        body = request.get_json(force=True)
        user = User.objects().get(id=user_id)
        user.update(**body)
        user.save()
        return Response(status=200)

    def delete(self, user_id):
        try:
            user = User.objects().get(id=user_id)
            user.delete()
            return Response(status=200)
        except DoesNotExist:
            raise UserNotExistsError


class UsersApi(Resource):

    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype='application/json', status=200)

    def post(self):
        body = request.get_json(force=True)
        user = User(**body)
        user.save()
        return Response(status=200)
