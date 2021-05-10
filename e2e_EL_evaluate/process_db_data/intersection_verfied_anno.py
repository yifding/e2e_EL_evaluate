# 1. Find the intersection of doc_names,
# 	a. Extract: “model2doc_name2dataset” and “model2dataset2doc_name”.
# 	b. Find the intersection “doc_name” for each (model, dataset) pair
#
# 2. For each (model, dataset) pair,
# 	a. extract “doc_name2txt, doc_name2anno” for each (model, dataset) pair.
# 	b. Only select the doc_name within the intersection.
#
# 3. For each (model, dataset) pair, given any “doc_name2txt, doc_name2anno”, find the corresponding subset

import os
import argparse

from e2e_EL_evaluate.utils.constants import (
    MODEL_NAMES,
    # DATASET_TYPES,
    # DATASET_TYPES2DATASET,
    DATASET2DATASET_TYPES,
)

from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.collect_dataset2doc_name import collect_dataset2doc_name
from e2e_EL_evaluate.utils.write_xml import write_xml


def main(args):
    # 1. Find the intersection of doc_names,
    # 1-a. Extract: “model2doc_name2dataset” and “model2dataset2doc_name”.
    model_name2dataset2doc_name, model_name2doc_name2dataset = collect_dataset2doc_name(
        args.label_xml_output_dir,
        identical=False,
    )
    # 1-b. Find the intersection “doc_name” for each (model, dataset) pair
    intersection_doc_names = set()
    first_model = MODEL_NAMES[0]
    for doc_name in model_name2doc_name2dataset[first_model]:
        INTER_FLAG = True
        for follow_model in MODEL_NAMES[1:]:
            assert follow_model in model_name2doc_name2dataset
            if doc_name not in model_name2doc_name2dataset[follow_model]:
                INTER_FLAG = False
                break
        if INTER_FLAG:
            intersection_doc_names.add(doc_name)
    print('len(intersection_doc_names)', len(intersection_doc_names))

    # 2. For each (model, dataset) pair,
    # 2-a. extract “doc_name2txt, doc_name2anno” for each (model, dataset) pair.
    # 2-b. Only select the doc_name within the intersection.
    # 3. For each (model, dataset) pair, given any “doc_name2txt, doc_name2anno”, find the corresponding subset
    for model in model_name2dataset2doc_name:
        for dataset in model_name2dataset2doc_name[model]:
            print('model: ', model, ' dataset: ', dataset)
            dataset_type = DATASET2DATASET_TYPES[dataset]

            label_xml_path = os.path.join(args.label_xml_output_dir, model + '/' + dataset_type)
            source_xml_path = os.path.join(args.rewrite_xml_output_dir, model + '/' + dataset_type)

            tmp_doc_name2txt, tmp_doc_name2anno = gen_anno_from_xml(label_xml_path, dataset)
            sub_doc_name2txt = dict()
            sub_doc_name2anno = dict()
            for doc_name in tmp_doc_name2txt:
                if doc_name in intersection_doc_names:
                    sub_doc_name2txt[doc_name] = tmp_doc_name2txt[doc_name]
                    sub_doc_name2anno[doc_name] = tmp_doc_name2anno[doc_name] if doc_name in tmp_doc_name2anno else {}

            tmp_source_doc_name2txt, tmp_source_doc_name2anno = gen_anno_from_xml(source_xml_path, dataset)
            sub_source_doc_name2anno = dict()
            for doc_name in sub_doc_name2txt:
                if doc_name in tmp_source_doc_name2anno:
                    sub_source_doc_name2anno[doc_name] = tmp_source_doc_name2anno[doc_name]

            intersect_xml_output_path = os.path.join(args.intersect_xml_output_dir, model + '/' + dataset_type)
            subset_ori_xml_output_path = os.path.join(args.subset_ori_xml_output_dir, model + '/' + dataset_type)
            write_xml(intersect_xml_output_path, dataset, sub_doc_name2txt, sub_doc_name2anno)
            write_xml(subset_ori_xml_output_path, dataset, sub_doc_name2txt, sub_source_doc_name2anno)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='process aida data to xml format',
            allow_abbrev=False,
    )

    parser.add_argument(
        '--rewrite_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/collect_pkl_rewrite_xml_EL',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--label_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/label_xml_EL',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--intersect_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/intersect_xml_EL',
        help='Specify the intersection output directory for the output xml',
    )

    parser.add_argument(
        '--subset_ori_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/intersect_subset_xml_EL',
        help='Specify the intersection output directory for the output xml',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.rewrite_xml_output_dir)
    assert os.path.isdir(args.label_xml_output_dir)

    os.makedirs(args.intersect_xml_output_dir, exist_ok=True)
    os.makedirs(args.subset_ori_xml_output_dir, exist_ok=True)

    main(args)



