import os
import pickle
import argparse


"""
    mysql> describe annotations; original annotations;
    +-------------+--------------+------+-----+---------+----------------+
    | Field       | Type         | Null | Key | Default | Extra          |
    +-------------+--------------+------+-----+---------+----------------+
    | id          | int(11)      | NO   | PRI | NULL    | auto_increment |
    | document_id | varchar(300) | YES  | MUL | NULL    |                |
    | model_enum  | varchar(200) | YES  |     | NULL    |                |
    | mention     | varchar(200) | YES  |     | NULL    |                |
    | entity      | varchar(200) | YES  |     | NULL    |                |
    | start_pos   | int(11)      | YES  |     | NULL    |                |
    | end_pos     | int(11)      | YES  |     | NULL    |                |
    +-------------+--------------+------+-----+---------+----------------+


    mysql> describe document; original documents (should not be changed in the whole process);
    +----------+----------------+------+-----+---------+-------+
    | Field    | Type           | Null | Key | Default | Extra |
    +----------+----------------+------+-----+---------+-------+
    | doc_id   | varchar(300)   | NO   | PRI | NULL    |       |
    | doc_body | varchar(15000) | YES  |     | NULL    |       |
    +----------+----------------+------+-----+---------+-------+


    mysql> describe document_annotation; annotated results; should perform post-processing to get standard format.
    +-------------+----------------+------+-----+---------+-------+
    | Field       | Type           | Null | Key | Default | Extra |
    +-------------+----------------+------+-----+---------+-------+
    | doc_id      | varchar(300)   | NO   | PRI | NULL    |       |
    | model_enum  | varchar(300)   | YES  |     | NULL    |       |
    | entire_text | varchar(15000) | YES  |     | NULL    |       |
    +-------------+----------------+------+-----+---------+-------+

    mysql> describe combinations_completed; document_id-model pair;
    +-------------+--------------+------+-----+---------+----------------+
    | Field       | Type         | Null | Key | Default | Extra          |
    +-------------+--------------+------+-----+---------+----------------+
    | id          | int(11)      | NO   | PRI | NULL    | auto_increment |
    | document_id | varchar(300) | YES  | MUL | NULL    |                |
    | model_enum  | varchar(100) | YES  |     | NULL    |                |
    | checked_out | tinyint(1)   | YES  |     | 0       |                |
    | completed   | tinyint(1)   | YES  |     | 0       |                |
    +-------------+--------------+------+-----+---------+----------------+

"""


def main(args):

    assert os.path.isdir(args.input_dir)
    doc_anno_file = os.path.join(args.input_dir, 'doc_anno.pkl')
    ori_doc_file = os.path.join(args.input_dir, 'ori_doc.pkl')
    ori_anno_file = os.path.join(args.input_dir, 'ori_anno.pkl')
    doc_model_pair_file = os.path.join(args.input_dir, 'doc_model_pair.pkl')

    doc_anno = pickle.load(open(doc_anno_file, "rb"))
    ori_doc = pickle.load(open(ori_doc_file, "rb"))
    ori_anno = pickle.load(open(ori_anno_file, "rb"))
    doc_model_pair = pickle.load(open(doc_model_pair_file, "rb"))

    print("doc_anno", len(doc_anno[0]), doc_anno[0], '\n')    # len=3
    print("ori_doc", len(ori_doc[0]), ori_doc[0], '\n')   # len=2
    print("ori_anno", len(ori_anno[0]), ori_anno[0], '\n')    # len=7
    print("doc_model_pair", len(doc_model_pair[0]), doc_model_pair[0], '\n')  # len=5


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

    args = parser.parse_args()
    main(args)