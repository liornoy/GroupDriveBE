from .users import UserApi, UsersApi
from .trips import TripApi, TripsApi
from .events import JoinTripApi, LoginApi


def initialize_routes(api):

    # Users API

    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<user_id>')

    # Trips API

    api.add_resource(TripsApi, '/api/trips')
    api.add_resource(TripApi, '/api/trips/<trip_id>')

    # Events API

    api.add_resource(JoinTripApi,
                     '/api/events/jointrip/<trip_id>')
    api.add_resource(LoginApi,
                     '/api/events/login')
   