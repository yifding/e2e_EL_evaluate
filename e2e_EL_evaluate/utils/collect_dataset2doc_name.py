"""
this function aims to extract dataset2doc_name from the standard xml EL layouts.

LAYOUTS:
    path/to/directory
    |
    |---model_name1
    |
    |---model_name2
        |
        |---dataset_type1
        |
        |---dataset_type2
            |
            |---dataset_name1
            |
            |---dataset_name2
                |
                |---dataset_name2.xml
                |
                |---RawText
                    |
                    |---doc_name1
                    |
                    |---doc_name2

Layout example:

/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/max_num_docs-1000/
    |
    |---end2end_neural_el
    |
    |---GT
        |
        |---aida
        |
        |---wned
            |
            |---ace2004
            |
            |---aquaint
                |
                |---aquaint.xml
                |
                |---RawText
                    |
                    |---APW19980816_0994.htm-1176_1484
                    |
                    |---APW19980930_0522.htm-438_843
"""

MODEL_NAMES = [
    'GT',
    'rel',
    'end2end_neural_el',
]

DATASET_TYPES = [
    'aida',
    'wned',
]



