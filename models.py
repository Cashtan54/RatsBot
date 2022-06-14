from peewee import *
from datetime import datetime

db = SqliteDatabase(None)


class BaseModel(Model):

    class Meta:
        database = db


class Food(BaseModel):
    name = CharField()
    is_allowed = BooleanField(default=True)
    description = CharField()


class User(BaseModel):
    username = CharField(unique=True)
    user_tg_id = IntegerField()
    start_time = DateTimeField(default=datetime.now())