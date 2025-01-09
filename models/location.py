from peewee import Model, AutoField, CharField, FloatField
from .db import db

class Location(Model):
    location_id = AutoField()
    location_name = CharField()
    latitude = FloatField()
    longitude = FloatField()

    class Meta:
        database = db 