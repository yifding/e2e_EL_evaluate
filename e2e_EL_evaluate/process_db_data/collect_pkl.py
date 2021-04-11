import os
import re
import html
import pickle
import argparse

from collections import defaultdict


DBModel2XMLModel = {
    'GT': 'GT',
    'REL': 'rel',
    'E2E': 'end2end_neural_el',
}

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


def collect_doc(ori_doc):
    """
    mysql> describe document; original documents (should not be changed in the whole process);
    +----------+----------------+------+-----+---------+-------+
    | Field    | Type           | Null | Key | Default | Extra |
    +----------+----------------+------+-----+---------+-------+
    | doc_id   | varchar(300)   | NO   | PRI | NULL    |       |
    | doc_body | varchar(15000) | YES  |     | NULL    |       |
    +----------+----------------+------+-----+---------+-------+

    :param ori_doc: list of tuples, [(doc_id, doc_body)]
    :return: doc_name2txt: a dictionary of txt, key is the name of the documents (from multiple datasets), value is the
    corresponding documentation text.
    """
    print('collecting original documents from DB list.')
    print(len(ori_doc), ' total documents are collected.')

    doc_name2txt = dict()
    for (doc_id, doc_body) in ori_doc:
        # repeated documentation is not allowed
        assert doc_id not in doc_name2txt
        doc_name2txt[doc_id] = doc_body
    return doc_name2txt


def collect_anno(ori_anno):
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

    :param ori_anno: list of tuples, [(id, document_id, model_enum, mention, entity, start_pos, end_pos)]
    :return: double2anno: a dictionary of list, each element of the list is a dictionary:
    {
        (model, doc_name): [
            {
                'start': start,
                'end': end,
                'mention_txt': mention,
                'entity_txt': entity,
            }
        ]
    }
    """
    print('collecting original annotations from DB list.')
    print(len(ori_anno), ' total annotations are collected.')

    double2anno = defaultdict(list)
    for (id, document_id, model_enum, mention, entity, start_pos, end_pos) in ori_anno:
        assert type(document_id) is str
        assert type(model_enum) is str
        assert type(mention) is str
        assert type(entity) is str
        assert type(start_pos) is int
        assert type(end_pos) is int

        double2anno[(model_enum, document_id)].append(
            {
                'start': start_pos,
                'end': end_pos,
                'mention_txt': mention,
                'entity_txt': entity,
            }
        )

    for key in double2anno:
        tmp_anno = double2anno[key]
        tmp_anno = sorted(tmp_anno, key=lambda x: (x['start'], x['end']))
        double2anno[key] = tmp_anno

    return double2anno


def old_process_entire_txt(entire_txt):
    """
    Core function to process the labelled text to obtain
    :param entire_txt: raw text with potential annotated entities.

    '<div style="background-color: yellow; display: inline;" id="1ZeqcTpSxhSG" data-annotation="https://en.wikipedia.org/wiki/Germany">German</div>

    :return: (anno_list, text) tuple,
    text: raw text without entity annotations
    anno_list: a list of annotations (dictionary)
    """
    txt = ''
    anno_list = []
    pre_pre = '<div style="background-color: yellow; display: inline;" id="'
    pre = 'data-annotation="https://en.wikipedia.org/wiki/'
    mid = '">'
    post = '</div>'

    cur_pos = 0
    pre_pre_pos = entire_txt.find(pre_pre, cur_pos)

    print('entire_txt:')
    print(repr(entire_txt))

    while pre_pre_pos >= 0:
        txt += entire_txt[cur_pos: pre_pre_pos]

        cur_pos = pre_pre_pos
        pre_pos = entire_txt.find(pre, cur_pos)
        entity_start = pre_pos + len(pre)

        mid_pos = entire_txt.find(mid, entity_start)
        assert mid_pos > entity_start

        entity = entire_txt[entity_start:mid_pos]
        mention_start = mid_pos + len(mid)
        post_pos = entire_txt.find(post, mention_start)

        assert post_pos > mention_start
        mention = entire_txt[mention_start:post_pos]

        anno_list.append(
            {
                'start': len(txt),
                'end': len(txt) + len(mention),
                'mention_txt': mention,
                'entity_txt': entity,
            }
        )

        txt += mention
        cur_pos = post_pos + len(post)

        pre_pre_pos = entire_txt.find(pre_pre, cur_pos)

    txt += entire_txt[cur_pos:]

    return txt, anno_list


def process_entire_txt(entire_txt):
    """
    Core function to process the labelled text to obtain, use regular expression to extract.
    :param entire_txt: raw text with potential annotated entities.

    '<div style="background-color: yellow; display: inline;" id="1ZeqcTpSxhSG" data-annotation="https://en.wikipedia.org/wiki/Germany">German</div>

    :return: (txt, anno_list) tuple,
    txt: raw text without entity annotations
    anno_list: a list of annotations (dictionary)
    """

    def process(s):
        return html.unescape(s)

    def extract(s):
        """
        :param s: r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="(.+)">(.+)</div>'
        :return: mention, entity

        txt: plain txt without annotations.
        """

        wiki_prefix = 'https://en.wikipedia.org/wiki/'
        pre = 'data-annotation="'
        mid = '">'
        post = '</div>'

        pre_pos = s.find(pre)
        mid_pos = s.find(mid)
        post_pos = s.find(post)
        assert 0 < pre_pos < mid_pos < post_pos

        mention = s[mid_pos + len(mid): post_pos]
        entity = s[pre_pos + len(pre): mid_pos]
        if entity.startswith(wiki_prefix):
            entity = entity[len(wiki_prefix):]
        else:
            entity = ''

        return mention, entity

    entire_txt = process(entire_txt)
    txt = ''
    anno_list = []
    cur_pos = 0

    r_s = r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="(.*?)">(.*?)</div>'
    # **YD** enhenced version of regular expression matching pattern.
    # r_s = r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="(((?!<div)(?!</div>).)+)</div>'

    for i in re.finditer(r_s, entire_txt):
        start = i.start()
        end = i.end()
        txt += entire_txt[cur_pos: start]
        cur_pos = end

        mention, entity = extract(entire_txt[start: end])

        if entity != '':
            anno_list.append(
                {
                    'start': len(txt),
                    'end': len(txt) + len(mention),
                    'mention_txt': mention,
                    'entity_txt': entity,
                }
            )
        txt += mention

    txt += entire_txt[cur_pos:]

    return txt, anno_list


def collect_doc_anno(doc_anno):
    """
    mysql> describe document_annotation; annotated results; should perform post-processing to get standard format.
    +-------------+----------------+------+-----+---------+-------+
    | Field       | Type           | Null | Key | Default | Extra |
    +-------------+----------------+------+-----+---------+-------+
    | doc_id      | varchar(300)   | NO   | PRI | NULL    |       |
    | model_enum  | varchar(300)   | YES  |     | NULL    |       |
    | entire_text | varchar(15000) | YES  |     | NULL    |       |
    +-------------+----------------+------+-----+---------+-------+

    :param doc_anno: list of tuples, [(doc_id, model_enum, entire_text)]
    :return: double2doc_anno, double2label_anno, double2label_text

    double2doc_anno: a dictionary of txt,
    double2label_anno: a dictionary of list,
    {
        (model, doc_name): [
            {
                'start': start,
                'end': end,
                'mention_txt': mention,
                'entity_txt': entity,
            }
        ]
    }

    double2label_text: a dictionary of list,

    {
        (model, doc_name): text,
    }

    """

    print('collecting labelled annotations from DB list.')
    print(len(doc_anno), ' total annotated texts are collected.')

    double2label_anno = dict()
    double2label_txt = dict()
    double2doc_anno = dict()

    for (doc_id, model_enum, entire_text) in doc_anno:
        txt, anno_list = process_entire_txt(entire_text)
        assert (model_enum, doc_id) not in double2doc_anno
        assert (model_enum, doc_id) not in double2label_anno
        assert (model_enum, doc_id) not in double2label_txt

        double2doc_anno[(model_enum, doc_id)] = entire_text
        double2label_anno[(model_enum, doc_id)] = anno_list
        double2label_txt[(model_enum, doc_id)] = txt

    return double2doc_anno, double2label_anno, double2label_txt


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

    double2doc_anno, double2label_anno, double2label_txt = collect_doc_anno(doc_anno)
    double2anno = collect_anno(ori_anno)
    doc_name2txt = collect_doc(ori_doc)

    model_set = set()
    for double in double2anno:
        model, doc_name = double
        model_set.add(model)
    print('DBModels', model_set)

    # **YD** Check 1: in double2label_txt, all the txts are equal to the doc_name2txt
    num_un_matched_txt = 0
    for double in double2label_txt:
        model, doc_name = double
        assert doc_name in doc_name2txt
        label_txt = double2label_txt[double]
        doc_anno = double2doc_anno[double]
        txt = doc_name2txt[doc_name]
        if label_txt != txt:
            print('model', model, 'doc_name', doc_name)
            print('doc_anno:')
            print(doc_anno)
            print('label_txt:')
            print(repr(label_txt))
            print('txt:')
            print(repr(txt))
            num_un_matched_txt += 1

    print(f'{num_un_matched_txt} / {len(double2label_txt)} are different txts!')


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