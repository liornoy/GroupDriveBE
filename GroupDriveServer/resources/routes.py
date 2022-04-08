from .users import UserApi, UsersApi
from .trips import (
    TripApi,
    TripsApi,
    JoinTripApi,
    UpdateCoordinatesAPI,
    GetCoordinatesAPI,
)


def initialize_routes(api):

    # Users API

    api.add_resource(UsersApi, "/api/users")
    api.add_resource(UserApi, "/api/users/<userId>")

    # Trips API

    api.add_resource(TripsApi, "/api/trips")
    api.add_resource(TripApi, "/api/trips/<tripId>")
    api.add_resource(JoinTripApi, "/api/trips/<tripId>/join")
    api.add_resource(UpdateCoordinatesAPI, "/api/trips/<tripId>/update-coordinates")
    api.add_resource(GetCoordinatesAPI, "/api/trips/<tripId>/get-coordinates")
