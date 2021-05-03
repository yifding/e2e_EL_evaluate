import os
import argparse

from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def extract_subset_xml(subset_xml_dir, subset_dataset, full_xml_dir, full_dataset):
    """
    :param subset_xml_dir: first dataset (must be a subset of second one).
    :param subset_dataset:
    :param full_xml_dir: second dataset.
    :param full_dataset:
    :return:
    """
    assert subset_dataset == full_dataset
    subset_doc_name2txt, subset_doc_name2anno = gen_anno_from_xml(subset_xml_dir, subset_dataset, allow_mention_without_entity=True)
    full_doc_name2txt, full_doc_name2anno = gen_anno_from_xml(full_xml_dir, full_dataset)

    # make sure the all doc_name exists in subset_doc_name2txt also in full_doc_name2txt
    # the texts are also the same.

    for doc_name in subset_doc_name2txt:
        assert doc_name in full_doc_name2txt
        assert subset_doc_name2txt[doc_name] == full_doc_name2txt[doc_name]

    full_new_doc_name2anno = dict()
    for doc_name in full_doc_name2anno:
        if doc_name in subset_doc_name2txt:
            full_new_doc_name2anno[doc_name] = full_doc_name2anno[doc_name]

    FLAG_EQUAL_TXT = True
    for doc_name in full_doc_name2txt:
        if doc_name not in subset_doc_name2txt:
            FLAG_EQUAL_TXT = False

    print('FLAG_EQUAL_TXT: ', FLAG_EQUAL_TXT)

    return subset_doc_name2txt, subset_doc_name2anno, full_new_doc_name2anno


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
        default='ace2004',
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
        default='ace2004',
        help='dataset for EL',
        choices=['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train'],
    )

    args = parser.parse_args()
    for dataset in ['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train']:
        if 'aida' in dataset:
            args.subset_xml_dir = '/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/label_xml_EL/GT/aida'
            args.full_xml_dir = '/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/collect_pkl_rewrite_xml_EL/GT/aida'
        else:
            args.subset_xml_dir = '/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/label_xml_EL/GT/wned'
            args.full_xml_dir = '/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/collect_pkl_rewrite_xml_EL/GT/wned'

        args.subset_dataset = args.full_dataset = dataset
        extract_subset_xml(args.subset_xml_dir, args.subset_dataset, args.full_xml_dir, args.full_dataset)