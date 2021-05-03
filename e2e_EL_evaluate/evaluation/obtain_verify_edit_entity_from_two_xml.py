import os
import argparse

from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES, XMLModel2DBModel
from e2e_EL_evaluate.evaluation.verify_edit_from_xml import EditEntityCount, edit_entity_from_xml
from e2e_EL_evaluate.utils.extract_subset_xml import extract_subset_xml


def obtain_edit_entity_from_two_xml(
    subset_xml_dir,
    subset_dataset,
    full_xml_dir,
    full_dataset,
):

    subset_doc_name2txt, subset_doc_name2anno, full_new_doc_name2anno = extract_subset_xml(
        subset_xml_dir,
        subset_dataset,
        full_xml_dir,
        full_dataset
    )

    edit_entity = edit_entity_from_xml(
        subset_doc_name2txt,
        subset_doc_name2anno,
        full_new_doc_name2anno,
    )

    return edit_entity


def main(args):

    verify = remove = edit = 0

    for model in args.models:
        assert model in XMLModel2DBModel
        for dataset in args.datasets:
            assert dataset in DATASET2DATASET_TYPES

            subset_xml_dir = os.path.join(
                args.subset_xml_dir,
                model + '/' + DATASET2DATASET_TYPES[dataset],
            )

            full_xml_dir = os.path.join(
                args.full_xml_dir,
                model + '/' + DATASET2DATASET_TYPES[dataset],
            )

            dataset_path = os.path.join(subset_xml_dir, dataset)

            print('dataset_path', dataset_path)
            if os.path.isdir(dataset_path):
                print('args.subset_xml_dir', subset_xml_dir)
                subset_dataset = full_dataset = dataset
                edit_entity = obtain_edit_entity_from_two_xml(
                    subset_xml_dir,
                    subset_dataset,
                    full_xml_dir,
                    full_dataset,
                )
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
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_2_2021/label_xml_EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--full_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_2_2021/collect_pkl_rewrite_xml_EL',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--models',
        type=eval,
        default="['GT','rel','end2end_neural_el']",
        help='models for EL',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        default="['ace2004','aquaint','clueweb','msnbc','wikipedia','aida_testa','aida_testb','aida_train']",
        help='datasets for EL',
    )

    args = parser.parse_args()
    main(args)
