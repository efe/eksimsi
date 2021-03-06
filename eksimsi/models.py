from peewee import *

db = SqliteDatabase("eksimsi.db")


class BaseModel(Model):
    class Meta:
        database = db


class Subject(BaseModel):
    eksi_id = IntegerField(unique=True)
    title = CharField(max_length=50)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.title


class Entry(BaseModel):
    eksi_id = IntegerField(unique=True)
    subject = ForeignKeyField(Subject, related_name="entries", null=True)
    content = TextField(null=True)
    author = CharField(max_length=40, null=True)
    start_datetime = DateTimeField(null=True)
    end_datetime = DateTimeField(null=True)
    is_crawled = BooleanField(default=False)

    class Meta:
        db_table = 'entries'

    def __str__(self):
        return "%s-%s" % (self.subject, self.eksi_id)

if __name__ == "__main__":
    try:
        Subject.create_table()
        print("Subject table is created.")
    except OperationalError:
        print("Subject table already exists!")

    try:
        Entry.create_table()
        print("Entry table is created.")
    except OperationalError:
        print("Album table already exists!")
