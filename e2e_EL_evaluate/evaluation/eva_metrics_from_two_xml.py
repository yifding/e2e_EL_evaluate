import os
import argparse

from e2e_EL_evaluate.evaluation.confusion_matrix_from_xml import ConfusionMatrix, confusion_matrix_from_xml
from e2e_EL_evaluate.utils.extract_subset_xml import extract_subset_xml


def main(args):
    subset_doc_name2txt, subset_doc_name2anno, full_new_doc_name2anno = extract_subset_xml(
        args.subset_xml_dir,
        args.subset_dataset,
        args.full_xml_dir,
        args.full_dataset
    )

    if len(subset_doc_name2txt) > 0:
        print('num_doc', len(subset_doc_name2txt))
        print('len_subset_doc_name2anno', sum(len(value) for value in subset_doc_name2anno.values()))
        print('len_full_doc_name2anno', sum(len(value) for value in full_new_doc_name2anno.values()))

        confusion_matrix = confusion_matrix_from_xml(
            subset_doc_name2txt,
            subset_doc_name2anno,
            full_new_doc_name2anno,
        )

        print('TP', confusion_matrix.TP)
        print('FP', confusion_matrix.FP)
        print('TN', confusion_matrix.TN)
        print('FN', confusion_matrix.FN)

        print('precision', confusion_matrix.precision)
        print('recall', confusion_matrix.recall)
        print('F1', confusion_matrix.F1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--subset_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/label_xml_EL/GT/wned',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--subset_dataset',
        type=str,
        default='aquaint',
        help='dataset for EL',
        choices=['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train'],
    )

    parser.add_argument(
        '--full_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/collect_pkl_rewrite_xml_EL/GT/wned',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--full_dataset',
        type=str,
        default='aquaint',
        help='dataset for EL',
        choices=['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train'],
    )

    args = parser.parse_args()
    main(args)