import requests

author_data = {'name': 'life'} 
author_resp = requests.get('http://127.0.0.1:5500/api/v1/genres')
authors = author_resp.json()
print(authors)
