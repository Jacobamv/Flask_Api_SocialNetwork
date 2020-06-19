import requests
import json

url = 'http://127.0.0.1:5000/api/login'
headers = {'Content-type': 'application/json'}
data = {"username" : "Jacob_amv", "password" : "qwerty123"}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
