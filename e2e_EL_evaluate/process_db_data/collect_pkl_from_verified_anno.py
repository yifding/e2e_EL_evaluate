import os
import re
import copy
import html
import pickle
import argparse

from collections import defaultdict

from e2e_EL_evaluate.utils.constants import DBModel2XMLModel, XMLModel2DBModel
from e2e_EL_evaluate.utils.collect_dataset2doc_name import collect_dataset2doc_name, DATASET2DATASET_TYPES
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.write_xml import write_xml
from e2e_EL_evaluate.utils.collect_db_pkl import (
    collect_doc_name2txt_from_doc,
    collect_double2anno_from_anno,
    collect_anno_id2anno_from_anno,
    collect_double2anno_from_verified_anno_and_anno_id2anno_from_anno,
)


def transform_fix_double2anno(double2anno, doc_name2dataset):
    """
    :param double2anno:
    :param doc_name2dataset:
    :return:
    :param fix_double2anno
    """

    fix_double2anno = defaultdict(dict)
    for double in double2anno:
        model, doc_name = double

        # **YD** transform to new the xml model name
        assert model in DBModel2XMLModel
        model = DBModel2XMLModel[model]
        if doc_name not in doc_name2dataset:
            print('doc_name', doc_name)
            print(list(doc_name2dataset.keys())[:100])
        assert doc_name in doc_name2dataset
        dataset = doc_name2dataset[doc_name]
        assert doc_name not in fix_double2anno[(model, dataset)]
        fix_double2anno[(model, dataset)][doc_name] = double2anno[double]

    return fix_double2anno


def transform_doc_name2txt(doc_name2txt, doc_name2dataset):
    dataset2txt = defaultdict(dict)
    for doc_name in doc_name2txt:
        if doc_name not in doc_name2dataset:
            print('doc_name', doc_name)
        assert doc_name in doc_name2dataset
        dataset = doc_name2dataset[doc_name]
        assert doc_name not in dataset2txt[dataset]

        dataset2txt[dataset][doc_name] = doc_name2txt[doc_name]

    return dataset2txt


def transform_fix_double2txt(double2txt, doc_name2dataset):
    fix_double2txt = defaultdict(dict)
    for double in double2txt:
        model, doc_name = double
        # **YD** transform to new the xml model name
        assert model in DBModel2XMLModel
        model = DBModel2XMLModel[model]
        assert doc_name in doc_name2dataset
        dataset = doc_name2dataset[doc_name]

        assert doc_name not in fix_double2txt[(model, dataset)]
        fix_double2txt[(model, dataset)][doc_name] = double2txt[double]

    return fix_double2txt


def main(args):

    assert os.path.isdir(args.input_dir)
    ori_doc_file = os.path.join(args.input_dir, 'ori_doc.pkl')
    ori_anno_file = os.path.join(args.input_dir, 'ori_anno.pkl')
    valid_verified_anno_file = os.path.join(args.input_dir, 'valid_verified_anno.pkl')

    # 1. extract "doc", "anno" and "valid_verified_anno".
    ori_doc = pickle.load(open(ori_doc_file, "rb"))
    ori_anno = pickle.load(open(ori_anno_file, "rb"))
    valid_verified_anno = pickle.load(open(valid_verified_anno_file, "rb"))

    assert len(ori_doc[0]) == 2
    assert len(ori_anno[0]) == 7
    assert len(valid_verified_anno[0]) == 8

    # 2. obtain "doc_name2txt", "double2anno", "double2anno_from_verified"
    doc_name2txt = collect_doc_name2txt_from_doc(ori_doc)
    double2anno = collect_double2anno_from_anno(ori_anno)
    anno_id2anno = collect_anno_id2anno_from_anno(ori_anno)
    double2anno_from_verified = collect_double2anno_from_verified_anno_and_anno_id2anno_from_anno(
        valid_verified_anno, anno_id2anno
    )

    # 3. extract the dataset2doc_name dictionary of list
    dataset2doc_name, doc_name2dataset = collect_dataset2doc_name(args.source_xml_dir)

    # 4. transform double to fix_double
    fix_double2anno = transform_fix_double2anno(double2anno, doc_name2dataset)
    fix_double2anno_from_verified = transform_fix_double2anno(double2anno_from_verified, doc_name2dataset)
    dataset2txt = transform_doc_name2txt(doc_name2txt, doc_name2dataset)

    # 5. CHECK: fix_double2anno_from_verified has the same number of annotations in each doc as fix_double2anno.
    num_total_docs = 0
    num_remove_docs = 0
    for index, fix_double in enumerate(fix_double2anno_from_verified):
        tmp_anno_from_verified = fix_double2anno_from_verified[fix_double]
        assert fix_double in fix_double2anno
        tmp_anno = fix_double2anno[fix_double]

        delete_key_list = []
        for doc_name in tmp_anno_from_verified:
            num_total_docs += 1
            assert doc_name in tmp_anno
            if len(tmp_anno_from_verified[doc_name]) != len(tmp_anno[doc_name]):
                num_remove_docs += 1
                delete_key_list.append(doc_name)

                # print(fix_double, doc_name, index)
                # print('tmp_anno_from_verified[doc_name]', tmp_anno_from_verified[doc_name])
                # print('tmp_anno[doc_name]', tmp_anno[doc_name])
                # raise ValueError('different length of annotaitons', len(tmp_anno_from_verified[doc_name]), len(tmp_anno[doc_name]))

        for tmp_key in delete_key_list:
            del fix_double2anno_from_verified[fix_double][tmp_key]

    print('num_total_docs', num_total_docs, 'num_remove_docs', num_remove_docs)
    # raise ValueError('by intention!')

    # 6. write "ori_doc" and "ori_anno" back to xml.
    for model in XMLModel2DBModel:
        for dataset in dataset2txt:
            assert dataset in DATASET2DATASET_TYPES
            prefix = os.path.join(args.rewrite_xml_output_dir, model + '/' + DATASET2DATASET_TYPES[dataset])
            tmp_doc_name2txt = dataset2txt[dataset]
            tmp_doc_name2anno = fix_double2anno[(model, dataset)] if (model, dataset) in fix_double2anno else {}

            # **YD** check each annotation has a valid mention.
            for tmp_doc_name in tmp_doc_name2anno:
                assert tmp_doc_name in tmp_doc_name2txt
                tmp_txt = tmp_doc_name2txt[tmp_doc_name]
                tmp_anno_list = tmp_doc_name2anno[tmp_doc_name]
                for tmp_anno in tmp_anno_list:
                    tmp_start = tmp_anno['start']
                    tmp_end = tmp_anno['end']
                    tmp_mention_txt = tmp_anno['mention_txt']
                    # tmp_entity_txt = tmp_anno['entity_txt']
                    assert tmp_mention_txt == tmp_txt[tmp_start: tmp_end]

            write_xml(prefix, dataset, tmp_doc_name2txt, tmp_doc_name2anno)

    # 7. write "fix_double2anno_from_verified" back to xml.
    # **YD** we only deal with the txt with at least on annotations. The txt is as anchor to select as subset.

    for fix_double in fix_double2anno_from_verified:
        model, dataset = fix_double
        assert dataset in DATASET2DATASET_TYPES
        assert model in XMLModel2DBModel

        prefix = os.path.join(args.label_xml_output_dir, model + '/' + DATASET2DATASET_TYPES[dataset])
        tmp_doc_name2txt = dict()
        tmp_doc_name2txt_from_dataset2txt = dataset2txt[dataset]
        for doc_name in fix_double2anno_from_verified[fix_double]:
            tmp_doc_name2txt[doc_name] = tmp_doc_name2txt_from_dataset2txt[doc_name]
        tmp_doc_name2anno = fix_double2anno_from_verified[fix_double]
        write_xml(prefix, dataset, tmp_doc_name2txt, tmp_doc_name2anno)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/download_db2disk',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--source_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--rewrite_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_2_2021/collect_pkl_rewrite_xml_EL',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--label_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_2_2021/label_xml_EL',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.input_dir)
    assert os.path.isdir(args.source_xml_dir)
    os.makedirs(args.rewrite_xml_output_dir, exist_ok=True)
    os.makedirs(args.label_xml_output_dir, exist_ok=True)
    main(args)
