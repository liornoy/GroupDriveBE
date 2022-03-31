from flask_restful import Resource
from flask import Response, request
from database.models import User


class UserApi(Resource):

    def get(self, id):
        user = User.objects().get(id=id)
        return Response(user, mimetype='application/json', status=200)

    def put(self, id):
        body = request.get_json(force=True)
        user = User.objects().get(id=id)
        user.update(**body)
        user.save()
        return Response(status=200)

class UsersApi(Resource):

    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype='application/json', status=200)

    def post(self):
        body = request.get_json(force=True)
        user = User(**body)
        user.save()
        return Response(status=200)
