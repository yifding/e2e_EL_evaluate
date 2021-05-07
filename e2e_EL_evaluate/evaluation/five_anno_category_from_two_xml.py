import os
import argparse


class AnnoFiveCategory(object):
    def __init__(self, c1, c2, c3, c4, c5):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5

        
def main(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--subset_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/label_xml_EL/GT/wned',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--subset_dataset',
        type=str,
        default='aquaint',
        help='dataset for EL',
        choices=['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train'],
    )

    parser.add_argument(
        '--full_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/collect_pkl_rewrite_xml_EL/GT/wned',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--full_dataset',
        type=str,
        default='aquaint',
        help='dataset for EL',
        choices=['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train'],
    )

    args = parser.parse_args()
    main(args)