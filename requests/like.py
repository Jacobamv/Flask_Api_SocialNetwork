import requests
import json

url = 'http://127.0.0.1:5000/api/comment/like'
headers = {'Content-type': 'application/json'}
data = {
	"comid" : 1
	}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
