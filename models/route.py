from peewee import Model, AutoField, CharField, ForeignKeyField, TextField, IntegerField
from .db import db
from .location import Location

class Route(Model):
    route_id = AutoField()
    route_name = CharField()
    start_location = ForeignKeyField(Location, backref='routes_from')
    end_location = ForeignKeyField(Location, backref='routes_to')
    connection_ids = TextField()  # コロン区切りの文字列
    total_time = IntegerField()

    class Meta:
        database = db 