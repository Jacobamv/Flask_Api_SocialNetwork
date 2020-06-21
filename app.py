from flask import Flask, jsonify, request, send_file, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, decode_token
)
from models import *
from peewee import *
import os


p =  os.path.abspath("app.py")
i = p.index("app.py")
p = p[:i] + "img"
app = Flask(__name__)
app.config['SECRET KEY'] = 'aoaooaoaoaoaoaoa'
app.config['UPLOAD_FOLDER'] = p
app.config['JWT_SECRET_KEY'] = 'aoaoaoaoaoaoaooaaooaoaoaoa'
jwt = JWTManager(app)


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/api/signup', methods = ['POST'])
def SignUp():

	if not request.is_json:
		return jsonify({"msg": "Missing JSON in request"})

	#id username password name email phone
	_username = request.json.get('username', None)
	_password = request.json.get('password', None)
	_name = request.json.get('name', None)
	_email = request.json.get('email', None)
	_phone = request.json.get('phone', None)
	access_token = create_access_token(identity=_username)
	us = Users( username = _username, password = _password, name = _name, email = _email, phone = _phone)
	us.save()

	return jsonify(access_token=access_token), 200


@app.route('/api/login', methods = ['POST'])
def LogIn():
	username = request.json.get('username')
	password = request.json.get('password')

	query = Users.select().where(Users.username == username)
	
	if not query.exists():
		return jsonify({"msg" : "DoesNotExist"})

	for i in query:
		if i.password == password:
			access_token = create_access_token(identity=i.username)
			return jsonify({"id": i.id, "username": i.username, "password" : i.password, "name" : i.name, "email" : i.email, "phone" : i.phone, "access_token" : access_token })

@app.route('/api/checktoken', methods = ['POST'])
def Check():

	username = request.json.get('username')
	token = request.json.get('access_token')

	access_token = create_access_token(identity = username)
	tokken = decode_token(token)

	if username == tokken['identity']:
		return jsonify({"msg" : "True"})
	else:
		return jsonify({"msg" : "False" })	

@app.route('/api/createpost', methods = ['POST'])
def CreatePost():
	username = request.json.get('username')
	_content = request.json.get('content')
	hasfile = request.json.get('hasfile')
	_title = request.json.get('title')
	_ownerid =  Users.select(Users.id).where(Users.username == username).get()
	file = ""
	if hasfile:
		f = request.files['file']
		n = secure_filename(f.filename)
		i = n.index('.')
		n = title + n[i:]
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],n))
		file = str(request.host)+ '/api/' + 'img' + '/' + n
	pst = Posts(ownerid = _ownerid, title = _title, content = _content, media = file, hasmedia = hasfile, ownerusername = username)
	pst.save()

	query = Users.update(CountOfPosts=Users.CountOfPosts + 1).where(Users.username == username)
	query.execute()

	return jsonify({"msg" : "ok"})

@app.route('/api/img/<filename>')
def GetImg(filename):
	return send_file('img/'+filename)


@app.route('/api/createcomment', methods = ['POST'])
def CreateComment():
	_postid = request.json.get('postid')
	_ownerid = request.json.get('ownerid')
	_ownerusername = request.json.get('ownerusername')
	_text = request.json.get('content')
	cmnt = Comments(postid = _postid, ownerid = _ownerid, text = _text, ownerusername = _ownerusername)
	cmnt.save()
	return jsonify({"msg" : "ok"})

@app.route('/api/getposts', methods = ['GET'])
def GetPosts():
	_username = request.json.get('username')
	_username = Users.select(Users.id).where(Users.username == _username).get()
	owners = []
	rl = Relations.select().where(Relations.first == _username)
	for i in rl:
		owners.append(i.second)
	owners.append(_username)

	posts = Posts.select().where(Posts.ownerid << owners).order_by(Posts.published)

	jsone = {"CountOfPosts" : len(posts), "Posts" : []}

	for i in posts:
		jsone["Posts"].append({
			"id" : i.id,
			"ownerid" : i.ownerid,
			"ownerusername" : i.ownerusername,
			"date" : i.published,
			"title" : i.title,
			"text" : i.content,
			"hasmedia" : i.hasmedia,
			"media" : i.media,
			"likes" : i.likes,
			"dislikes" : i.dislikes,
			"comments" : []
			#id ownerid published title content hasmedia media likes dislikes
			})  
		cm = Comments.select().where(Comments.postid == i.id)
		for j in cm:
			jsone["Posts"][-1]["comments"].append({
				"id" : j.id,
				"postid" : j.postid,
				"ownerid" : j.ownerid,
				"ownerusername" : j.ownerusername,
				"text" : j.text,
				"likes" : j.likes,
				"dislikes" : j.dislikes
			#	id postid ownerid text likes dislikes 
			})
	return jsonify(jsone)

@app.route("/api/post/like", methods=['POST'])
def LikePost():
	_postid = request.json.get("postid")
	query = Posts.update(likes=Posts.likes + 1).where(Posts.id == _postid)
	query.execute()
	return jsonify({"msg" : "ok"})

@app.route("/api/post/dislike", methods=['POST'])
def DislikePost():
	_postid = request.json.get("postid")
	query = Posts.update(dislikes=Posts.dislikes + 1).where(Posts.id == _postid)
	query.execute()
	return jsonify({"msg" : "ok"})

@app.route("/api/comment/like", methods=['POST'])
def LikeComment():
	_comid = request.json.get("comid")
	query = Comments.update(likes=Comments.likes + 1).where(Comments.id == _comid)
	query.execute()
	return jsonify({"msg" : "ok"})

@app.route("/api/comment/dislike", methods=['POST'])
def DislikeComment():
	_comid = request.json.get("comid")
	query = Comments.update(dislikes=Comments.dislikes + 1).where(Comments.id == _comid)
	query.execute()
	return jsonify({"msg" : "ok"})

@app.route("/api/getfriends", methods=['GET'])
def GetFriends():
	_username = request.json.get('username')
	friends = []
	rl = Relations.select().where(Relations.first == _username)
	for i in rl:
		friends.append(i.second)

	json = {"CountOfFriends" : len(friends), "friends" : []}
	for i in friends:
		j = Users.select().where(Users.username == i).get()
		json["friends"].append({
			"id" : j['id'],
			"username" : j.username
		})
	return jsonify(json)

@app.route("/api/newrel", methods = ['POST'])
def NewRelation():
	_first = request.json.get('who')
	_second = request.json.get('with')

	rel = Relations(first = _first, second= _second)
	rel.save()

	query = Users.update(CountOfFriends=Users.CountOfFriends + 1).where(Users.username == _first)
	query.execute()

	return jsonify({"msg" : "ok"})

@app.route("/api/gethost", methods = ['GET'])
def GetHost():
	return jsonify({"host" : request.host})