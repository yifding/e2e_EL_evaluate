import os
import argparse

from e2e_EL_evaluate.utils.write_xml import write_xml
from e2e_EL_evaluate.utils.check_xml_anno import check_xml_anno
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def main(args):
    print('input directory: ', args.input_dir, 'output dir: ', args.output_dir)
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)

    for dataset in args.datasets:
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset, has_prob=args.input_has_prob)
        check_xml_anno(doc_name2txt, doc_name2anno)
        write_xml(args.output_dir, dataset, doc_name2txt, doc_name2anno, has_prob=args.output_has_prob)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/wned/xml/ori_xml2revise_xml",
        type=str,
    )

    parser.add_argument(
        "--output_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/wned/xml/revise_xml2el_xml",
        type=str,
    )

    parser.add_argument(
        "--datasets",
        default="['ace2004','aquaint','clueweb','msnbc','wikipedia']",
        type=eval,
    )
    parser.add_argument(
        "--input_has_prob",
        action="store_true",
    )
    parser.add_argument(
        "--output_has_prob",
        action="store_true",
    )

    args = parser.parse_args()
    main(args)