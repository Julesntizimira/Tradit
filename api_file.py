#!/usr/bin/python3
import requests

url = 'http://localhost:5000/books' 

req = requests.post(url, data={'name':'The Alchemist', 'description':'advanture'})

r = req.json()
print(r)
