import peewee
from local import DB


class Page(peewee.Model):
    id = peewee.IntegerField()
    url = peewee.TextField()
    status = peewee.IntegerField()
    content_type = peewee.CharField(max_length=128)
    links = peewee.TextField()

    class Meta:
        database = DB
