import os
import argparse

from e2e_EL_evaluate.utils.write_xml import write_xml
from e2e_EL_evaluate.utils.check_xml_anno import check_xml_anno
from e2e_EL_evaluate.utils.read_aida_conll import read_aida_conll


AIDA_TRAIN_FILE = "aida_train.txt"
AIDA_TEST_FILE = "testa_testb_aggregate_original"


def process_aida_train(args):
    aida_train_file = os.path.join(args.input_dir, AIDA_TRAIN_FILE)
    text_dict_train, redict_train = read_aida_conll(aida_train_file)

    write_xml(args.output_dir, 'aida_train', text_dict_train, redict_train)


def process_aida_test(args):
    aida_test_file = os.path.join(args.input_dir, AIDA_TEST_FILE)
    text_dict, redict = read_aida_conll(aida_test_file)

    text_dict_testa = dict()
    text_dict_testb = dict()

    redict_testa = dict()
    redict_testb = dict()

    for doc_name in text_dict:
        if 'testa' in doc_name:
            text_dict_testa[doc_name] = text_dict[doc_name]
        elif 'testb' in doc_name:
            text_dict_testb[doc_name] = text_dict[doc_name]
        else:
            raise ValueError("unknown document")

    for doc_name in redict:
        if 'testa' in doc_name:
            redict_testa[doc_name] = redict[doc_name]
        elif 'testb' in doc_name:
            redict_testb[doc_name] = redict[doc_name]
        else:
            raise ValueError("unknown document")

    print('check aida_testa:')
    check_xml_anno(text_dict_testa, redict_testa)

    print('check aida_testb:')
    check_xml_anno(text_dict_testb, redict_testb)

    # write aida_testa
    write_xml(args.output_dir, 'aida_testa', text_dict_testa, redict_testa)
    write_xml(args.output_dir, 'aida_testb', text_dict_testb, redict_testb)


def main(args):
    print('input directory: ', args.input_dir, 'output dir: ', args.output_dir)
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    process_aida_train(args)
    process_aida_test(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/EL_resource/data/raw/AIDA-CONLL',
        help='Specify the input AIDA directory',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/ori_token2trans_span',
        help='Specify the input AIDA directory',
    )
    args = parser.parse_args()
    main(args)