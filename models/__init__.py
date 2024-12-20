from peewee import SqliteDatabase
from .db import db
from .example import Example

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [Example]


def initialize_exampledb():
    Example(message='hello world').save()


# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    initialize_exampledb()
    db.close()
