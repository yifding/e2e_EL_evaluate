import os
import random
import argparse
from collections import defaultdict

from e2e_EL_evaluate.utils.write_xml import write_xml
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def main(args):
    assert os.path.isdir(args.input_dir)
    args.output_dir = os.path.join(args.output_dir, "max_num_docs-{}".format(args.max_num_docs))
    os.makedirs(args.output_dir, exist_ok=True)

    # triple means (model, dataset, doc_name) triples
    triple2txt = dict()
    triple2anno = dict()
    triple2select = dict()

    for model in args.models:
        for dataset in args.datasets:
            parts = dataset.split('/')
            assert len(parts) == 2
            suffix, dataset = parts[0], parts[1]
            input_dir = os.path.join(args.input_dir, model + '/' + suffix)
            doc_name2txt, doc_name2anno = gen_anno_from_xml(input_dir, dataset)

            for doc_name in doc_name2txt:
                triple2select[model, dataset, doc_name] = 0
                triple2txt[model, dataset, doc_name] = doc_name2txt[doc_name]

            for doc_name in doc_name2anno:
                triple2anno[model, dataset, doc_name] = doc_name2anno[doc_name]

    random.seed(args.seed)
    keys = list(triple2select.keys())
    random.shuffle(keys)

    print('total document is: ', len(keys))
    for key in keys[:args.max_num_docs]:
        triple2select[key] = 1

    print(len(keys[:args.max_num_docs]), 'over total doc: ', len(keys), ' is selected !!!')

    # filter out triple2txt and triple2anno
    for triple in triple2select:
        if triple2select[triple] == 0:
            assert triple in triple2txt
            del triple2txt[triple]
            if triple in triple2anno:
                del triple2anno[triple]

    # write back the txt and annotations.
    double2txt = defaultdict(dict)
    double2anno = defaultdict(dict)

    for triple in triple2txt:
        model, dataset, doc_name = triple
        double2txt[model, dataset][doc_name] = triple2txt[triple]

    for triple in triple2anno:
        model, dataset, doc_name = triple
        double2anno[model, dataset][doc_name] = triple2anno[triple]


    for model in args.models:
        for dataset in args.datasets:
            parts = dataset.split('/')
            assert len(parts) == 2
            suffix, dataset = parts[0], parts[1]
            output_dir = os.path.join(args.output_dir, model + '/' + suffix)

            if (model, dataset) in double2txt:
                print('write to xml: model', model, 'dataset', dataset)
                doc_name2txt = double2txt[model, dataset]
                doc_name2anno = double2anno[model, dataset]
                write_xml(output_dir, dataset, doc_name2txt, doc_name2anno)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL',
        help='Specify the input xml annotation directory',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/',
        help='Specify the input xml annotation directory',
    )

    parser.add_argument(
        '--models',
        type=eval,
        default='["end2end_neural_el", "GT", "rel"]',
        help='model sub dirs under the input_dir',
    )

    parser.add_argument(
        "--datasets",
        default="['aida/aida_testa', 'aida/aida_testb', 'aida/aida_train',"
                "'wned/ace2004', 'wned/aquaint', 'wned/clueweb', 'wned/msnbc', 'wned/wikipedia',]",
        type=eval,
    )

    parser.add_argument(
        "--max_num_docs",
        default=1000,
        type=int,
    )

    parser.add_argument(
        "--seed",
        default=19940802,
        type=int,
    )

    args = parser.parse_args()
    main(args)