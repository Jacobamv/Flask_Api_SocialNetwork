from peewee import *
import datetime
db = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
	id = IntegerField(primary_key=True)
	username = CharField()
	password = CharField()
	name = CharField()
	email = CharField()
	phone = CharField(default = "")
	CountofPosts = IntegerField(default=0)
	CountofFriends = IntegerField(default=0)

class Posts(BaseModel):
	id = IntegerField(primary_key=True)
	ownerid = CharField()
	ownerusername = CharField()
	published = DateField(default = datetime.datetime.now())
	title = CharField()
	content = TextField()
	hasmedia = BooleanField() 
	media = CharField()
	likes = IntegerField(default = 0)
	dislikes = IntegerField(default = 0)

class Comments(BaseModel):
	id = IntegerField(primary_key = True)
	postid = CharField()
	ownerid = CharField()
	ownerusername = CharField()
	text = TextField()
	likes = IntegerField(default = 0)
	dislikes = IntegerField(default = 0)

class Relations(BaseModel):
	id = IntegerField(primary_key = True)
	first = CharField()
	second = CharField()

Users.create_table()
Posts.create_table()
Comments.create_table()
Relations.create_table()

