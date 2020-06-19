import requests
import json

url = 'http://127.0.0.1:5000/api/createpost'
headers = {'Content-type': 'application/json'}
data = {
	"username" : "Jacob_amv", 
	"content" : "Jacob luchshiy backend proger",
	"hasfile" : False,
	"title" : "Jacob luchshiy backend proger"

	}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
