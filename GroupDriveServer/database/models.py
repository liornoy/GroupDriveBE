from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField, \
    FloatField, DateTimeField, BooleanField


class User(Document):

    photoURL = StringField()
    name = StringField(required=True)


class Trip(Document):

    creator = ReferenceField('User')
    meetingPoint = StringField(required=True)
    meetingPointWazeUrl = StringField(required=True)
    description = StringField(required=True)
    participants = ListField(ReferenceField('User'))
    date = DateTimeField(required=True)
    isTripToday = BooleanField(required=True, default=False)


class UserLiveGPSCoordinate(Document):

    user = ReferenceField('User')
    trip = ReferenceField('Trip')
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)
