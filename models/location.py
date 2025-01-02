from peewee import Model, AutoField, CharField
from .db import db

class Location(Model):
    location_id = AutoField()
    location_name = CharField()

    class Meta:
        database = db 