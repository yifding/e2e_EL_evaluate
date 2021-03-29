import os
import argparse

from e2e_EL_evaluate.utils.xml2stanza_token import xml2stanza_token


def tokenize(args):
    assert os.path.isdir(args.input_dir)

    for dataset in args.datasets:
        xml2stanza_token(args.input_dir, dataset, args.output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/wned/xml/ori_xml2revise_xml",
        type=str,
    )

    parser.add_argument(
        "--output_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/wned/conll/revise_xml2trans_token",
        type=str,
    )

    parser.add_argument(
        "--datasets",
        default="['ace2004','aquaint','clueweb','msnbc','wikipedia']",
        type=eval,
    )

    args = parser.parse_args()
    tokenize(args)