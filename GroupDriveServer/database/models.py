from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ReferenceField,
    ListField,
    FloatField,
    DateTimeField,
    BooleanField,
    IntField,
)
from datetime import datetime as dt
from mongoengine.errors import DoesNotExist
from json import dumps


class User(Document):
    googleID = StringField(required=True, primary_key=True)
    photoURL = StringField()
    name = StringField(required=True)
    # preferences = DictField(required=True)


class Trip(Document):
    tripID = IntField(required=True, primary_key=True)
    title = StringField(required=True)
    creatorGID = StringField(required=True)
    meetingPoint = StringField(required=True)
    meetingPointWazeUrl = StringField()
    description = StringField()
    participants = ListField(StringField())
    dateTime = DateTimeField(required=True)
    isTripToday = BooleanField(default=False)

    def updateTrip(self):
        if self.dateTime.date() == dt.today().date():
            self.isTripToday = True
            self.save()

    def isUserJoined(self, user_GID):
        for p in self.participants:
            if p == user_GID:
                return True
        return False

    def addUser(self, user_GID):
        self.participants.append(user_GID)
        self.save()

    def getParticipantsCoordinates(self):
        coordinates = []
        for p in self.participants:
            try:
                c = UserLiveGPSCoordinates.objects().get(userGID=p)
            except DoesNotExist:
                continue
            coordinates += [c.to_json()]
        return coordinates


class UserLiveGPSCoordinates(Document):
    userGID = StringField(required=True)
    tripID = IntField(required=True)
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)

    def isValid(self):
        trip = Trip.objects().get(tripID=self.tripID)

        joinedTrip = trip.isUserJoined(self.userGID)
        isTripToday = trip.isTripToday
        return joinedTrip and isTripToday
