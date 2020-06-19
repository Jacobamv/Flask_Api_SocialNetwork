import requests
import json

url = 'http://127.0.0.1:5000/api/createcomment'
headers = {'Content-type': 'application/json'}
data = {
	"postid" : 1,
	"ownerid" : 2,
	"content" : "Jacob luchshiy proger",
	"ownerusername" : "Jacob_amv"
	}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
