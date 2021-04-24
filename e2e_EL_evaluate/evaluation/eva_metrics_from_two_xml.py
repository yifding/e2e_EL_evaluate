import os
import argparse

from e2e_EL_evaluate.utils.collect_dataset2doc_name import DATASET2DATASET_TYPES
from e2e_EL_evaluate.evaluation.confusion_matrix_from_xml import ConfusionMatrix, confusion_matrix_from_xml
from e2e_EL_evaluate.utils.extract_subset_xml import extract_subset_xml


def eva_metrics_from_two_xml(args):
    subset_doc_name2txt, subset_doc_name2anno, full_new_doc_name2anno = extract_subset_xml(
        args.subset_xml_dir,
        args.subset_dataset,
        args.full_xml_dir,
        args.full_dataset
    )

    """
    if len(subset_doc_name2txt) > 0:
        print('num_doc', len(subset_doc_name2txt))
        print('len_subset_doc_name2anno', sum(len(value) for value in subset_doc_name2anno.values()))
        print('len_full_doc_name2anno', sum(len(value) for value in full_new_doc_name2anno.values()))
    """
    confusion_matrix = confusion_matrix_from_xml(
        subset_doc_name2txt,
        subset_doc_name2anno,
        full_new_doc_name2anno,
    )

    print('TP', confusion_matrix.TP)
    print('FP', confusion_matrix.FP)
    print('TN', confusion_matrix.TN)
    print('FN', confusion_matrix.FN)

    num_subset_anno = sum(len(value) for value in subset_doc_name2anno.values())
    num_full_anno = sum(len(value) for value in full_new_doc_name2anno.values())
    if num_subset_anno > 0 and num_full_anno > 0:
        print('precision', confusion_matrix.precision)
        print('recall', confusion_matrix.recall)
        print('F1', confusion_matrix.F1)

    return confusion_matrix


def main(args):

    TP = FP = TN = FN = 0
    for split in ['accept', 'reject']:
        # for model in ['GT', 'rel', 'end2end_neural_el']:
        for model in ['end2end_neural_el']:
            for dataset in ['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train']:
                assert dataset in DATASET2DATASET_TYPES

                args.subset_xml_dir = '/scratch365/yding4/e2e_EL_evaluate/data/4_23_2021/label_xml/'\
                                      + split + '/' + model + '/' + DATASET2DATASET_TYPES[dataset]

                args.full_xml_dir = '/scratch365/yding4/e2e_EL_evaluate/data/4_23_2021/rewrite_xml/' \
                                    + split + '/' + model + '/' + DATASET2DATASET_TYPES[dataset]

                dataset_path = os.path.join(args.subset_xml_dir, dataset)
                if os.path.isdir(dataset_path):
                    print('args.subset_xml_dir', args.subset_xml_dir)
                    args.subset_dataset = args.full_dataset = dataset
                    confusion_matrix = eva_metrics_from_two_xml(args)

                    TP += confusion_matrix.TP
                    FP += confusion_matrix.FP
                    TN += confusion_matrix.TN
                    FN += confusion_matrix.FN

    confusion_matrix = ConfusionMatrix(TP, TN, FP, FN)
    print('TP', confusion_matrix.TP)
    print('FP', confusion_matrix.FP)
    print('TN', confusion_matrix.TN)
    print('FN', confusion_matrix.FN)


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
    #eva_metrics_from_two_xml(args)