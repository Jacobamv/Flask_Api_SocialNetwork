import requests
import json

url = 'http://127.0.0.1:5000/api/newrel'
headers = {'Content-type': 'application/json'}
data = {"who" : "Jacob_am",	"with" : "Jacob_amv"}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
