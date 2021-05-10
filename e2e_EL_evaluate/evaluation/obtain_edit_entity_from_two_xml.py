import os
import argparse

from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES
from e2e_EL_evaluate.evaluation.edit_entity_from_xml import EditEntityCount, edit_entity_from_xml
from e2e_EL_evaluate.utils.extract_subset_xml import extract_subset_xml


def obtain_edit_entity_from_two_xml(args):
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
    edit_entity = edit_entity_from_xml(
        subset_doc_name2txt,
        subset_doc_name2anno,
        full_new_doc_name2anno,
    )

    # print('verify', edit_entity.verify)
    # print('remove', edit_entity.remove)
    # print('edit', edit_entity.edit)

    return edit_entity


def main(args):

    verify = remove = edit = 0
    for split in ['accept', 'reject']:
    # for split in ['reject']:
        #for model in ['GT', 'rel', 'end2end_neural_el']:
        for model in ['rel']:
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
                    edit_entity = obtain_edit_entity_from_two_xml(args)

                    verify += edit_entity.verify
                    edit += edit_entity.edit
                    remove += edit_entity.remove

    print('verify', verify)
    print('remove', remove)
    print('edit', edit)


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