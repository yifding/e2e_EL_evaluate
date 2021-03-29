import os
import argparse

from e2e_EL_evaluate.utils.write_xml import write_xml
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def main(args):
    print('input directory: ', args.input_dir, 'output dir: ', args.output_dir)
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)

    for dataset in args.datasets:
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset)
        write_xml(args.output_dir, dataset, doc_name2txt, doc_name2anno)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/ori_token2trans_span",
        type=str,
    )

    parser.add_argument(
        "--output_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span",
        type=str,
    )

    parser.add_argument(
        "--datasets",
        default="['aida_train', 'aida_testa', 'aida_testb']",
        type=eval,
    )

    args = parser.parse_args()
    main(args)