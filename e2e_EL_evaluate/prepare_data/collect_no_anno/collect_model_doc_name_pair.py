import os
import pickle
import argparse

from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.constants import XMLModel2DBModel, DATASET2DATASET_TYPES


def collect_model_doc_name_pair(args):
    num_total = 0
    model_doc_pair = []
    for model in args.models:
        assert model in XMLModel2DBModel
        db_model = XMLModel2DBModel[model]
        for dataset in args.datasets:
            print('(model, dataset)', (model, dataset))
            assert dataset in DATASET2DATASET_TYPES
            dataset_type = DATASET2DATASET_TYPES[dataset]
            prefix = os.path.join(args.input_dir, model + '/' + dataset_type + '/')
            doc_name2txt, doc_name2anno = gen_anno_from_xml(prefix, dataset)

            for doc_name in doc_name2txt:
                num_total += 1
                if doc_name not in doc_name2anno or len(doc_name2anno[doc_name]) == 0:
                    pair = (db_model, doc_name)
                    assert pair not in model_doc_pair
                    model_doc_pair.append(pair)

    output_file = os.path.join(args.output_dir, args.output_file)
    pickle.dump(model_doc_pair, open(output_file, "wb"))

    print('number of total documents is: ', num_total, 'number of documents without annotation is: ', len(model_doc_pair))
    print(model_doc_pair)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL',
        help='Specify the input xml data dir',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split',
        help='',
    )

    parser.add_argument(
        '--output_file',
        type=str,
        default='EL_no_anno_model_doc_name_pair.pickle',
        help='',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        default="['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']",
        help='datasets to processed',
    )

    parser.add_argument(
        '--models',
        type=eval,
        default="['GT', 'rel', 'end2end_neural_el']",
        help='models to processed',
    )

    args = parser.parse_args()

    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    collect_model_doc_name_pair(args)
