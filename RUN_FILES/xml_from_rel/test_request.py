import requests

# API_URL = "https://rel.cs.ru.nl/api"
API_URL = "http://127.0.0.1:1235"
text_doc = "If you're going to try, go all the way - Charles Bukowski - Barak Obama"

# Example EL.
el_result = requests.post(API_URL, json={
    "text": text_doc,
    "spans": []
}).json()

"""
# Example ED.
ed_result = requests.post(API_URL, json={
    "text": text_doc,
    "spans": [(41, 16)]
}).json()
"""

print(el_result)
# print(ed_result)