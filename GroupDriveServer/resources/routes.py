from .users import SignIn,SignUp, UsersApi
from .trips import (
    TripApi,
    TripsApi,
    JoinTripApi,
    UpdateCoordinatesAPI,
    GetCoordinatesAPI,
    PostMessageAPI,
)


def initialize_routes(api):

    # Users API

    api.add_resource(UsersApi, "/api/users")
    api.add_resource(SignIn, "/api/users/sign-in/<username>/<password>")
    api.add_resource(SignUp, "/api/users/sign-up/<username>/<password>")
    #api.add_resource(Userget, "/api/users/<userID>")


    # Trips API

    api.add_resource(TripsApi, "/api/trips")
    api.add_resource(TripApi, "/api/trips/<tripId>")
    api.add_resource(JoinTripApi, "/api/trips/<tripId>/join")
    api.add_resource(UpdateCoordinatesAPI, "/api/trips/<tripId>/update-coordinates")
    api.add_resource(GetCoordinatesAPI, "/api/trips/<tripId>/get-coordinates")
    api.add_resource(PostMessageAPI, "/api/trips/<tripId>/live-messages")
