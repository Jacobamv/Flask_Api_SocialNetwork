import requests
import json

url = 'http://127.0.0.1:5000/api/signup'
headers = {'Content-type': 'application/json'}
data = {"username" : "Jacob_amv", "password" : "qwerty123", "name" : "Jacob", "email" : "jacob.akhmedov@gmail.com", "phone" : "+992928560139"}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
