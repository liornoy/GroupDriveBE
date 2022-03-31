errors = {
    'InternalServerError': {'message': 'Something went wrong',
                            'status': 500},
    'SchemaValidationError': {'message': 'Request is missing required fields',
                              'status': 400},
    'UpdatingTripError': {'message': 'Updating trip added by other is forbidden',
                          'status': 403},
    'DeletingTripError': {'message': 'Deleting trip added by other is forbidden',
                          'status': 403},
    'TripNotExistsError': {'message': "Trip with given id doesn't exists",
                           'status': 400},
    'UserAlreadyExistsError': {'message': 'User already exists',
                               'status': 400},
    'UnauthorizedError': {'message': 'Invalid username or password',
                          'status': 401},
    'UserNotExistsError': {'message': "User with given id doesn't exists",
                           'status': 400},
    'UpdatingUserError': {'message': 'Updating other user is forbidden',
                          'status': 403},
    'BadTokenError': {'message': 'Invalid token', 'status': 403},
    'ExpiredTokenError': {'message': 'Expired token', 'status': 403},
    }


class InternalServerError(Exception):

    pass


class SchemaValidationError(Exception):

    pass


class UpdatingTripError(Exception):

    pass


class DeletingTripError(Exception):

    pass


class TripNotExistsError(Exception):

    pass


class UserAlreadyExistsError(Exception):

    pass


class UnauthorizedError(Exception):

    pass


class UserNotExistsError(Exception):

    pass


class UpdatingUserError(Exception):

    pass

class BadTokenError(Exception):

    pass


class ExpiredTokenError(object):

    pass
