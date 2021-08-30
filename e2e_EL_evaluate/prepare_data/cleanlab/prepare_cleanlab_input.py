"""
INPUT:
    a. Pre-annotated original xml with prob:  /scratch365/yding4/e2e_EL_evaluate/data/has_prob/prepare_split/end2end_neural
    b. Pre-annotated original xml without prob:  /scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL/end2end_neural_el
    c. Post-annotated xml without prob:  /scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL/end2end_neural_el

OUTPUT:
    each dataset outputs a json file which contains
    {
		"signature": text name + start_index + end_index:
		    {
            "prob":
            "entity_before_anno":
            "entity_after_anno":
            "correctness":
		}
    }

"""

import os
import json
import argparse

from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def doc_name2anno_to_signature(doc_name2anno, has_prob=False):
    re_dict = dict()
    for doc_name in doc_name2anno:
        anno_list = doc_name2anno[doc_name]
        for anno in anno_list:
            start = anno['start']
            end = anno['end']
            signature = doc_name + '-' + str(start) + '_' + str(end)
            re_dict[signature] = {
                'entity_txt': anno['entity_txt']
            }
            if has_prob:
                re_dict[signature]['prob'] = anno['prob']
    return re_dict


def prepare_cleanlab_input(
    intersect_xml_EL_dir,
    intersect_subset_xml_EL_dir,
    ori_xml_EL_with_prob_dir,
    output_file,
    dataset,
):
    _, intersect_xml_EL_doc_name2anno = gen_anno_from_xml(intersect_xml_EL_dir, dataset, has_prob=False)
    _, intersect_subset_xml_doc_name2anno = gen_anno_from_xml(intersect_subset_xml_EL_dir, dataset, has_prob=False)
    _, ori_xml_EL_with_prob_doc_name2anno = gen_anno_from_xml(ori_xml_EL_with_prob_dir, dataset, has_prob=True)

    intersect_xml_EL_dict = doc_name2anno_to_signature(intersect_xml_EL_doc_name2anno, has_prob=False)
    intersect_subset_xml_EL_dict = doc_name2anno_to_signature(intersect_subset_xml_doc_name2anno, has_prob=False)
    ori_xml_EL_with_prob_dict = doc_name2anno_to_signature(ori_xml_EL_with_prob_doc_name2anno, has_prob=True)


    json_dict = dict()

    # print("intersect_xml_EL_dict", list(intersect_xml_EL_dict.items())[:5])
    # print("ori_xml_EL_with_prob_dict", list(ori_xml_EL_with_prob_dict.items())[:5])

    for signature in intersect_xml_EL_dict:
        if signature not in ori_xml_EL_with_prob_dict:
            continue

        prob = ori_xml_EL_with_prob_dict[signature]["prob"]
        entity_before_anno = intersect_xml_EL_dict[signature]["entity_txt"]
        entity_after_anno = ""
        if signature in intersect_subset_xml_EL_dict:
            if intersect_subset_xml_EL_dict[signature]["entity_txt"] != "NIL":
                entity_after_anno = intersect_subset_xml_EL_dict[signature]["entity_txt"]
        if entity_before_anno == entity_after_anno:
            correctness = True
        else:
            correctness = False

        value = {
            "prob": prob,
            "entity_before_anno": entity_before_anno,
            "entity_after_anno": entity_after_anno,
            "correctness": correctness,
        }
        json_dict[signature] = value

    json_dict = dict(sorted(json_dict.items(), key=lambda x: x[0]))
    with open(output_file, 'w') as writer:
        writer.write(json.dumps(json_dict, indent=4))


def main():
    args = parse_args()
    # intersect_xml_EL_dir = "/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL/end2end_neural_el/aida"
    # intersect_subset_xml_EL_dir = "/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL/end2end_neural_el/aida"
    # ori_xml_EL_with_prob_dir = "/scratch365/yding4/e2e_EL_evaluate/data/has_prob/prepare_split/end2end_neural"
    # output_dir = "/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input"
    # os.makedirs(output_dir, exist_ok=True)

    for dataset in args.datasets:
        output_file = dataset + ".json"
        output_file = os.path.join(args.output_dir, output_file)
        prepare_cleanlab_input(
            intersect_xml_EL_dir=args.intersect_xml_EL_dir,
            intersect_subset_xml_EL_dir=args.intersect_subset_xml_EL_dir,
            ori_xml_EL_with_prob_dir=args.ori_xml_EL_with_prob_dir,
            output_file=output_file,
            dataset=dataset,
        )


def parse_args():
    parser = argparse.ArgumentParser(allow_abbrev=False,)
    parser.add_argument(
        "--intersect_xml_EL_dir",
        required=True,
        # default="/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL/end2end_neural_el/aida",
        type=str,
    )
    parser.add_argument(
        "--intersect_subset_xml_EL_dir",
        required=True,
        # default="/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL/end2end_neural_el/aida",
        type=str,
    )
    parser.add_argument(
        "--ori_xml_EL_with_prob_dir",
        required=True,
        # default="/scratch365/yding4/e2e_EL_evaluate/data/has_prob/prepare_split/end2end_neural",
        type=str,
    )
    parser.add_argument(
        "--output_dir",
        required=True,
        # default="/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input",
        type=str,
    )
    parser.add_argument(
        "--datasets",
        required=True,
        # default="['ace2004']",
        type=eval,
    )
    args = parser.parse_args()
    assert os.path.isdir(args.intersect_xml_EL_dir)
    assert os.path.isdir(args.intersect_subset_xml_EL_dir)
    assert os.path.isdir(args.ori_xml_EL_with_prob_dir)
    assert type(args.datasets) is list

    os.makedirs(args.output_dir, exist_ok=True)

    return args


if __name__ == "__main__":
    main()
