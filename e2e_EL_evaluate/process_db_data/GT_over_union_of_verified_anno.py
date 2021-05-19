import os
import argparse
from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES, XMLModel2DBModel
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.five_types_EL_anno import five_types_EL_anno
# [1] based on intersection of doc_names and datasets.
# [2] obtain the union of annotations.
# [3] obtain GT annotations.
# [4] compare [3] and [4] to obtain a-f stats


def main(args):
    # [2] obtain the union of annotations.
    for dataset in DATASET2DATASET_TYPES:
        print('dataset: ', dataset)
        assert dataset in DATASET2DATASET_TYPES
        dataset_type = DATASET2DATASET_TYPES[dataset]
        union_doc_name2txt = dict()
        union_doc_name2anno = dict()
        for xml_model in XMLModel2DBModel:
            input_dir = os.path.join(args.input_verify_dir, xml_model + '/' + dataset_type)
            doc_name2txt, doc_name2anno = gen_anno_from_xml(input_dir, dataset)
            for doc_name in doc_name2txt:
                if doc_name not in union_doc_name2txt:
                    union_doc_name2txt[doc_name] = doc_name2txt[doc_name]
                else:
                    assert union_doc_name2txt[doc_name] == doc_name2txt[doc_name]

            for doc_name in doc_name2anno:
                if doc_name not in union_doc_name2anno:
                    union_doc_name2anno[doc_name] = []
                for anno in doc_name2anno[doc_name]:
                    if anno not in union_doc_name2anno[doc_name]:
                        union_doc_name2anno[doc_name].append(anno)

        # [3] obtain GT annotations.
        for model in args.models:
            model_xml_dir = os.path.join(args.model_xml_dir, model + '/' + dataset_type)
            model_doc_name2txt, model_doc_name2anno = gen_anno_from_xml(model_xml_dir, dataset)

            # [4] compare [3] and [4] to obtain a-f stats
            GT_union_stat = five_types_EL_anno(model_doc_name2anno, union_doc_name2anno)
            union_GT_stat = five_types_EL_anno(union_doc_name2anno, model_doc_name2anno)
            print('model: ', model)
            print(GT_union_stat)
            print(union_GT_stat)


def parse_args():
    parser = argparse.ArgumentParser(
        description='list the six categories of annotation between GT and union of verified annotations',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--input_verify_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_xml_EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--model_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_subset_xml_EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--models',
        type=eval,
        default="['GT']",
        #   default="['rel','GT','end2end_neural_el']",
        help='Specify the splits output directory for the db download file',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.input_verify_dir)
    assert os.path.isdir(args.model_xml_dir)

    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)
