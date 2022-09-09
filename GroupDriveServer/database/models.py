from mongoengine import Document
from mongoengine.fields import (
    StringField,
    ListField,
    FloatField,
    DateField,
    BooleanField,
    IntField,
    DateTimeField,
)
from datetime import datetime as dt
from bson.json_util import dumps


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
    maxGroupSize = IntField(default = -1)
    tripFull = BooleanField(default=False)

    def update_trip(self):
        if self.date == dt.today().date():
            self.isTripToday = True
        else:
            self.isTripToday = False
        if len(self.participants) == self.maxGroupSize:
            self.tripFull = True
        else:
            self.tripFull = False
        self.save()

    def is_user_joined(self, creator):
        for p in self.participants:
            if p == creator:
                return True
        return False

    def add_user(self, username):
        if self.is_user_joined(username) == False and not self.tripFull:
            self.participants.append(str(username))
            self.save()
        else: 
            self.participants.remove(str(username))
            coors = UserLiveGPSCoordinates.objects(tripID = self._id, user = str(username))
            if coors:
                coors.delete()
            if self.tripFull:
                self.tripFull = False
            self.save()

    def get_participants_coordinates(self):
        coors =  UserLiveGPSCoordinates.objects(tripID = self._id)
        c_list = []
        for c in coors:
            c_dict = c.to_mongo().to_dict()
            c_list.append(c_dict)
        coors_json=dumps(c_list)
        return coors_json
  


class UserLiveGPSCoordinates(Document):
    _id = StringField(required=True, primary_key=True)
    user = StringField(required=True)
    tripID = StringField(required=True)
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)

    def is_valid(self):
        trip = Trip.objects().get(_id=self.tripID)

        joinedTrip = trip.is_user_joined(self.user)
        isTripToday = trip.isTripToday
        return joinedTrip and isTripToday

class LiveMessages(Document):
    tripID = StringField(required=True)
    message = StringField(required=True)
    timeStamp = IntField(required=True)