from .users import onLogin, onEditUser, onShowUsers
from .trips import onEditTrip, onShowTrips, onJoinTrip

def initialize_routes(api):
    # Users API
    api.add_resource(onLogin, '/api/users/login')
    api.add_resource(onEditUser, '/api/users/<user_id>/edit')
    api.add_resource(onShowUsers, '/api/users')
    # Trips API
    api.add_resource(onShowTrips, '/api/trips')
    api.add_resource(onJoinTrip, '/api/trips/<trip_id>/join/<user_id>')
    api.add_resource(onEditTrip, '/api/trips/<trip_id>/edit')
