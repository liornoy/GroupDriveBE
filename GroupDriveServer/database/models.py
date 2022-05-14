from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ListField,
    FloatField,
    DateField,
    BooleanField,
)
from datetime import datetime as dt
from mongoengine.errors import DoesNotExist


class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    # preferences = DictField(required=True)


class Trip(Document):
    _id = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    creator = StringField(required=True)
    meetingPoint = StringField(required=True)
    meetingPointWazeUrl = StringField()
    description = StringField()
    participants = ListField(StringField())
    date = DateField(required=True, default=dt.today)
    isTripToday = BooleanField(default=False)

    def updateTrip(self):
        if self.date == dt.today().date():
            self.isTripToday = True
        else:
            self.isTripToday = False
        self.save()

    def isUserJoined(self, creator):
        for p in self.participants:
            if p == creator:
                return True
        return False

    def addUser(self, username):
        if self.isUserJoined(username) == False:
            print("added", username)
            self.participants.append(str(username))
            self.save()
        else:
            self.participants.remove(str(username))
            print("removed", username)
            self.save()

  


class UserLiveGPSCoordinates(Document):
    _id = StringField(required=True, primary_key=True)
    user = StringField(required=True)
    tripID = StringField(required=True)
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)

    def isValid(self):
        trip = Trip.objects().get(_id=self.tripID)

        joinedTrip = trip.isUserJoined(self.user)
        isTripToday = trip.isTripToday
        return joinedTrip and isTripToday
