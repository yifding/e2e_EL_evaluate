import os
import argparse
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def main(args):
    for dataset in args.datasets:
        print('dataset: ', dataset)
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset)
        print('num_of_docs_from_txt: ', len(doc_name2txt))

        num_docs_from_anno = 0
        for doc_name in doc_name2anno:
            if len(doc_name2anno[doc_name]) > 0:
                num_docs_from_anno += 1
        print('num_of_docs_from_anno: ', num_docs_from_anno)



def parse_args():
    parser = argparse.ArgumentParser(
        description='process aida data to xml format',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span',
        help='Specify the input xml data dir',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        # default="['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']",
        default="['aida_testa','aida_testb','aida_train']",
        help='datasets to processed',
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)

