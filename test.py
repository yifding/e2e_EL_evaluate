import json
import requests

myjson = { "text": "Obama will visit Germany and have a meeting with Merkel tomorrow.", "spans": []}
#r = requests.post("http://localhost:5555", json=myjson)
r = requests.post("http://127.0.0.1:1235", json=myjson)
output = r.content.decode("utf-8")
#output = requests.post("http://localhost:5555", json=myjson).content.decode("utf-8")

print(type(output), type(eval(output)), eval(output))
