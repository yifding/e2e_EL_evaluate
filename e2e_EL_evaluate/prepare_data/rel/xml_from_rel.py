import os
import json
import argparse
import requests
from collections import defaultdict

from tqdm import tqdm

from e2e_EL_evaluate.utils.write_xml import write_xml
from e2e_EL_evaluate.utils.check_xml_anno import check_xml_anno
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def process_anno(ori_anno_list, txt, has_prob=False):
    """
    :param ori_anno_list: like: [[0, 5, 'Obama', 'Barack_Obama', 0.0, 0.9997133612632751, 'PER'],
    [17, 7, 'Germany', 'Germany', 0.0, 0.9999783039093018, 'LOC']]
    :param txt:
    :param has_prob: # **YD-CL** whether extract ED probability.
    :return: standard anno_list for e2e_EL_evaluate.
    """
    anno_list = list()
    for anno in ori_anno_list:
        offset = anno[0]
        length = anno[1]
        labelled_mention = anno[2]
        entity_txt = anno[3]
        mention_txt = txt[offset: offset + length]
        assert labelled_mention == mention_txt
        assert len(mention_txt) == length

        ele = {
            'start': offset,
            'end': offset + length,
            'mention_txt': mention_txt,
            'entity_txt': entity_txt,
        }
        if has_prob:
            ele['prob'] = anno[4]   # the ED probability is at index 4
        anno_list.append(ele)

    anno_list = sorted(anno_list, key=lambda x: (x['start'],x['end']))
    return anno_list


def main(args):
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    for dataset in args.datasets:
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset)
        new_doc_name2anno = dict()

        for doc_name in tqdm(doc_name2txt):
            txt = doc_name2txt[doc_name]
            myjson = { "text": txt, "spans": []}
            ori_anno_list = eval(requests.post(args.URL, json=myjson).content.decode("utf-8"))
            anno_list = process_anno(ori_anno_list, txt, has_prob=args.has_prob)
            new_doc_name2anno[doc_name] = anno_list

        check_xml_anno(doc_name2txt, new_doc_name2anno)
        write_xml(args.output_dir, dataset, doc_name2txt, new_doc_name2anno, has_prob=args.has_prob)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        default="/home/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span",
        type=str,
    )

    parser.add_argument(
        "--output_dir",
        default="/home/yding4/e2e_EL_evaluate/data/aida/xml/xml_from_rel",
        type=str,
    )

    parser.add_argument(
        "--datasets",
        default="['aida_train','aida_testa','aida_testb']",
        type=eval,
    )

    parser.add_argument(
        "--URL",
        default="http://127.0.0.1:1235",
        type=str,
    )
    parser.add_argument(
        "--has_prob",
        action="store_true",
    )

    args = parser.parse_args()
    main(args)
