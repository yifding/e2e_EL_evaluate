import os
import pickle
import argparse

from db_util import DataBaseQueryUtil


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)

    '''
    doc_anno_file = 'doc_anno.pkl'
    ori_doc_file = 'ori_doc.pkl'
    ori_anno_file = 'ori_anno.pkl'
    '''

    doc_anno_file = os.path.join(args.output_dir, 'doc_anno.pkl')
    ori_doc_file = os.path.join(args.output_dir, 'ori_doc.pkl')
    ori_anno_file = os.path.join(args.output_dir, 'ori_anno.pkl')

    db_util = DataBaseQueryUtil()

    doc_anno = db_util.fetch(db_util.query_doc_anno)
    ori_doc = db_util.fetch(db_util.query_ori_doc)
    ori_anno = db_util.fetch(db_util.query_ori_anno)

    pickle.dump(doc_anno, open(doc_anno_file, "wb"))
    pickle.dump(ori_doc, open(ori_doc_file, "wb"))
    pickle.dump(ori_anno, open(ori_anno_file, "wb"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    '''
    parser.add_argument(
        '--input_dir',
        type=str,
        default='/home/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span',
        help='Specify the input xml annotation directory',
    )
    '''

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/home/yding4/e2e_EL_evaluate/data/download_db2disk',
        help='Specify the splits output directory for the db download file',
    )

    args = parser.parse_args()
    main(args)