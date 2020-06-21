import requests
import json

url = 'http://127.0.0.1:5000/api/getposts'
headers = {'Content-type': 'application/json'}
data = {
	"username" : 'Jacob_amv'
	}
answer = requests.get(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
