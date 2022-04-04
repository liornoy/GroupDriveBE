from mongoengine import Document
from mongoengine.fields import StringField, ReferenceField, ListField, \
    FloatField, DateTimeField, BooleanField, DictField
from datetime import datetime as dt

class User(Document):
    googleID = StringField()
    photoURL = StringField()
    name = StringField(required=True)
    preferences = DictField(required=True)

class Trip(Document):

    creator = ReferenceField('User')
    meetingPoint = StringField(required=True)
    meetingPointWazeUrl = StringField(required=True)
    description = StringField(required=True)
    participants = ListField(ReferenceField('User'))
    dateTime = DateTimeField(required=True)
    isTripToday = BooleanField(required=True, default=False)

    def updateTrip(self):
        if self.dateTime.date() == dt.today().date():
                self.isTripToday = True
                self.save()

    def isUserJoined(self, user):
        for p in self.participants:
            if p.googleID == user.googleID:
                return True
        return False



class UserLiveGPSCoordinates(Document):

    user = ReferenceField('User')
    trip = ReferenceField('Trip')
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)

    def isValid(self, user_id):
        auth = self.user.googleID == user_id
        joinedTrip = self.trip.isUserJoined(self.user)
        isTripToday = self.trip.isTripToday
        return auth and joinedTrip and isTripToday