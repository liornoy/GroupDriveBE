from .users import onLogin, onEditUser
from .trips import onEditTrip, onShowTrips, onJoinTrip

def initialize_routes(api):
    # Users API
    api.add_resource(onLogin, '/api/users/login')
    api.add_resource(onEditUser, '/api/users/<user_id>/edit')

    # Trips API
    api.add_resource(onShowTrips, '/api/trips')
    api.add_resource(onJoinTrip, '/api/trips/<trip_id>/join/<user_id>')
    api.add_resource(onEditTrip, '/api/trips/<trip_id>/edit')
