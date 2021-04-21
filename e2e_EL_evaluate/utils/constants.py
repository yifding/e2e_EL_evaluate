MODEL_NAMES = [
    'GT',
    'rel',
    'end2end_neural_el',
]

DATASET_TYPES = [
    'aida',
    'wned',
]

DATASET_TYPES2DATASET = {
    'aida': ['aida_testa', 'aida_testb', 'aida_train'],
    'wned': ['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia'],
}

DATASET2DATASET_TYPES = {
    'aida_testa': 'aida',
    'aida_testb': 'aida',
    'aida_train': 'aida',

    'ace2004': 'wned',
    'aquaint': 'wned',
    'clueweb': 'wned',
    'msnbc': 'wned',
    'wikipedia': 'wned',
}

DBModel2XMLModel = {
    'GT': 'GT',
    'REL': 'rel',
    'E2E': 'end2end_neural_el',
}

XMLModel2DBModel = {
    'GT': 'GT',
    'rel': 'REL',
    'end2end_neural_el': 'E2E',
}