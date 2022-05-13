from flask_restful import Resource
from flask import Response, request
from .errors import UserNotExistsError
from mongoengine.errors import DoesNotExist
from database.models import User, UserLiveGPSCoordinates
class SignIn(Resource):
    def post(self, username, password):
        try:
            print("signin got: ",username," and ", password)
            user = User.objects().get(username=username, password= password)
            return Response(str(username), mimetype="application/json", status=200)
        except DoesNotExist:
            return Response("error", mimetype="application/json", status=500)

class SignUp(Resource):
    def post(self, username, password):
        try:
            print("signup got: ",username," and ", password)
            user = User.objects().get(username=username)
        except DoesNotExist:
            newUser = User()
            newUser.username = username
            newUser.password = password
            newUser.save()
            return Response(str(username), mimetype="application/json", status=200)
        return Response("error", mimetype="application/json", status=500)
        
# class Userget(Resource):
#     def get(self,username):
#         try:
#             user = User.objects().get(userID = userID)
#             return Response(str(user.username), mimetype="application/json", status=200)
#         except DoesNotExist:
#             return Response("error", mimetype="application/json", status=500)


class UsersApi(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)