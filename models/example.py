from peewee import Model, CharField, DecimalField
from .db import db


class Example(Model):
    message = CharField()

    class Meta:
        database = db
