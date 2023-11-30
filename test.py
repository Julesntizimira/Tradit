import requests

req = requests.get('http://127.0.0.1:5500/api/v1/books')
print(req.json())