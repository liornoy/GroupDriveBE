from .db import db


class User(db.Document):
    photoURL = db.StringField()
    name = db.StringField(required=True)

class Trip(db.Document):
    creator = db.ReferenceField('User')
    meetingPoint = db.StringField(required=True)
    meetingPointWazeUrl= db.StringField(required=True)
    description= db.StringField(required=True)
    date= db.StringField(required=True)
    isTripToday=db.BooleanField(required=True, default=False)