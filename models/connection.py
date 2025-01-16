from peewee import Model, AutoField, ForeignKeyField, IntegerField
from .db import db
from .location import Location

class Connection(Model):
    connection_id = AutoField()
    from_location = ForeignKeyField(Location, backref='from_connections')
    to_location = ForeignKeyField(Location, backref='to_connections')
    travel_time = IntegerField()  # 移動時間（分）

    class Meta:
        database = db 