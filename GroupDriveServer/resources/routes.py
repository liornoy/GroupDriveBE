from users import UserApi, UsersApi
from trips import TripApi, TripsApi
from events import JoinTripEvent


def initialize_routes(api):

    # Users API

    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<id>')

    # Trips API

    api.add_resource(TripsApi, '/api/trips')
    api.add_resource(TripApi, '/api/trips/<id>')

    # Events API

    api.add_resource(JoinTripEvent,
                     '/api/events/jointrip/<user_id>/<trip_id>')
