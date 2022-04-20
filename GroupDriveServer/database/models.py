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
    googleID = StringField(required=True, primary_key=True)
    photoURL = StringField()
    name = StringField(required=True)
    # preferences = DictField(required=True)


class Trip(Document):
    tripID = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    creatorGID = StringField(required=True)
    meetingPoint = StringField(required=True)
    meetingPointWazeUrl = StringField()
    description = StringField()
    participants = ListField(StringField())
    date = DateField(required=True)
    isTripToday = BooleanField(default=False)

    def updateTrip(self):
        if self.date == dt.today().date():
            self.isTripToday = True
        else:
            self.isTripToday = False
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
    tripID = StringField(required=True)
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)

    def isValid(self):
        trip = Trip.objects().get(tripID=self.tripID)

        joinedTrip = trip.isUserJoined(self.userGID)
        isTripToday = trip.isTripToday
        return joinedTrip and isTripToday
