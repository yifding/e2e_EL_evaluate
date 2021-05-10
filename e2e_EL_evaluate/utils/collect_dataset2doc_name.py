import os
from collections import defaultdict

from e2e_EL_evaluate.utils.constants import (
    MODEL_NAMES,
    DATASET_TYPES,
    DATASET_TYPES2DATASET,
    DATASET2DATASET_TYPES,
)


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


def collect_dataset2doc_name(input_dir, identical=True):
    model_name2dataset2doc_name = dict()
    model_name2doc_name2dataset = dict()

    for model_name in MODEL_NAMES:

        dataset2doc_name = defaultdict(set)
        doc_name2dataset = dict()

        model_name_dir = os.path.join(input_dir, model_name)
        assert os.path.isdir(model_name_dir)

        for dataset_type in DATASET_TYPES2DATASET:
            for dataset in DATASET_TYPES2DATASET[dataset_type]:
                raw_text_path = os.path.join(model_name_dir, dataset_type + '/' + dataset + '/' + 'RawText')
                assert os.path.isdir(raw_text_path)
                for doc_name in os.listdir(raw_text_path):

                    # **YD** make sure one dataset has no repeated doc_name.
                    assert doc_name not in dataset2doc_name
                    dataset2doc_name[dataset].add(doc_name)
                    assert doc_name not in doc_name2dataset
                    doc_name2dataset[doc_name] = dataset

        model_name2dataset2doc_name[model_name] = dataset2doc_name
        model_name2doc_name2dataset[model_name] = doc_name2dataset

    if identical:
        for i in range(len(MODEL_NAMES) - 1):
            model_name1 = MODEL_NAMES[i]
            for j in range(i + 1, len(MODEL_NAMES)):
                model_name2 = MODEL_NAMES[j]

                assert model_name2dataset2doc_name[model_name1] == model_name2dataset2doc_name[model_name2]
                assert model_name2doc_name2dataset[model_name1] == model_name2doc_name2dataset[model_name2]

        return model_name2dataset2doc_name[MODEL_NAMES[0]], model_name2doc_name2dataset[MODEL_NAMES[0]]

    else:
        return model_name2dataset2doc_name, model_name2doc_name2dataset


if __name__ == '__main__':
    input_dir = '/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/collect_pkl_rewrite_xml_EL'
    collect_dataset2doc_name(input_dir, identical=True)
    input_dir = '/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/label_xml_EL'
    collect_dataset2doc_name(input_dir, identical=False)
