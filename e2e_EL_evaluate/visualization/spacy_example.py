import spacy
from spacy import displacy

a = {
    "text": "But Google is starting from behind.",
    "ents": [{"start": 4, "end": 10, "label": "Google"}],
    "title": ''
}

displacy.render(a, style='ent',manual=True)
displacy.serve(a, style='ent',manual=True)