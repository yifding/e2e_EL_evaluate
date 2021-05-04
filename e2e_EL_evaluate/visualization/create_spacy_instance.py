import os
import argparse
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def create_vis_instance(prefix, dataset, doc_name, title=''):
    doc_name2txt, doc_name2anno = gen_anno_from_xml(prefix, dataset)

    assert doc_name in doc_name2txt
    txt = doc_name2txt[doc_name]
    anno = doc_name2anno[doc_name] if doc_name in doc_name2anno else []

    ents = []
    for anno_ele in anno:
        start = anno_ele['start']
        end = anno_ele['end']
        mention = anno_ele['mention_txt']
        entity = anno_ele['entity_txt']

        assert txt[start:end] == mention
        ent = {
            'start': start,
            'end': end,
            'label': entity,
        }
        ents.append(ent)

    instance = {
        "text": txt,
        "ents": ents,
        'title': title,
    }

    print(repr(instance))
    return instance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
            '--input_dir',
            type=str,
            default='/scratch365/yding4/e2e_EL_evaluate/data/5_2_2021/collect_pkl_rewrite_xml_EL/GT/wned',
            help='Specify the splits output directory for the output xml directory from DB process results',
        )

    parser.add_argument(
        '--dataset',
        type=str,
        default='msnbc',
        choices=['ace2004','aquaint','clueweb','msnbc','wikipedia','aida_testa','aida_testb','aida_train'],
        help='dataset for EL',
    )

    parser.add_argument(
        '--doc_name',
        type=str,
        default='13259309-2336_2828',
        help='documentation name within the dataset',
    )

    args = parser.parse_args()

    create_vis_instance(args.input_dir, args.dataset, args.doc_name, title='')