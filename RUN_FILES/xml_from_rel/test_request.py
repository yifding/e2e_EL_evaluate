import requests

# API_URL = "https://rel.cs.ru.nl/api"  # for rel remote
# API_URL = "http://127.0.0.1:1235" # for rel local
API_URL = "http://localhost:5555"   # for end2end_neural_el

# text_doc = "If you're going to try, go all the way - Charles Bukowski - Barak Obama"

text_doc = "Obama will visit Germany and have a meeting with Merkel tomorrow."
# Example EL.
"""
el_result = requests.post(API_URL, json={
    "text": text_doc,
    "spans": []
}).json()
"""

el_result = eval(requests.post(API_URL, json={
    "text": text_doc,
    "spans": [],
}).content.decode("utf-8"))

"""
# Example ED.
ed_result = requests.post(API_URL, json={
    "text": text_doc,
    "spans": [(41, 16)]
}).json()
"""

print(el_result)
# print(ed_result)