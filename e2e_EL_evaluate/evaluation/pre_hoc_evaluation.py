import os
import argparse

from e2e_EL_evaluate.evaluation.confusion_matrix_from_xml import (
    confusion_matrix_from_xml,
    compute_metric,
)
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES, XMLModel2DBModel


def main(args):
    for dataset in DATASET2DATASET_TYPES:
        dataset_type = DATASET2DATASET_TYPES[dataset]
        model_xml_path = os.path.join(args.model_xml_dir, args.model_model + '/' + dataset_type)
        GT_xml_path = os.path.join(args.model_xml_dir, args.GT_model + '/' + dataset_type)
        model_doc_name2txt, model_doc_name2anno = gen_anno_from_xml(model_xml_path, dataset)
        GT_doc_name2txt, GT_doc_name2anno = gen_anno_from_xml(GT_xml_path, dataset)

        stats = confusion_matrix_from_xml(
        model_doc_name2txt,
        model_doc_name2anno,
        GT_doc_name2anno,
        is_strong_match=False,
        )

        metrics = compute_metric(stats)
        print('dataset: ', dataset)
        print(metrics)


def parse_args():
    parser = argparse.ArgumentParser(
        description='list the six categories of annotation between GT and union of verified annotations',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--model_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/collect_pkl_rewrite_xml_EL',
        help='Specify the splits input directory for the db download file',
    )

    parser.add_argument(
        '--GT_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/collect_pkl_rewrite_xml_EL',
        help='Specify the splits input directory for the db download file',
    )

    parser.add_argument(
        '--model_model',
        type=str,
        default='end2end_neural_el',
        choices=['rel','GT','end2end_neural_el'],
        help='Specify the model of model',
    )

    parser.add_argument(
        '--GT_model',
        type=str,
        default='GT',
        choices=['rel', 'GT', 'end2end_neural_el'],
        help='Specify the model of GT',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.model_xml_dir)
    assert os.path.isdir(args.GT_xml_dir)

    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)