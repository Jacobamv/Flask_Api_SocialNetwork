import requests
import json

url = 'http://127.0.0.1:5000/api/checktoken'
headers = {'Content-type': 'application/json'}
data = {"username" : "Jacob_amv", 'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTIzNzYxMjIsIm5iZiI6MTU5MjM3NjEyMiwianRpIjoiNTA4ZTVjNGEtNDk2Ni00ZTIyLWI0MGUtZjFiYTY1YzFkOTBhIiwiZXhwIjoxNTkyMzc3MDIyLCJpZGVudGl0eSI6IkphY29iX2FtdiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.d9KhBTYitLdEoGqXypk8nvZxWXAMDqlwu3fVmsTXxks'}
answer = requests.post(url, data=json.dumps(data), headers=headers)
print(answer)
response = answer.json()
print(response)
