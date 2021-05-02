from collections import defaultdict
from urllib.parse import unquote


def process_wiki_url(url):
    pre = 'https://en.wikipedia.org/wiki/'
    if url == '':
        return ''
    else:
        if not url.startswith(pre):
            print('Wrong input wikipedia url: ', url)
            return ''
        url = url[len(pre):]
        url = unquote(url).replace('_', ' ')
    return url


def collect_doc_name2txt_from_doc(ori_doc):
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


def collect_double2anno_from_anno(ori_anno):
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

        anno = {
                'start': start_pos,
                'end': end_pos,
                'mention_txt': mention,
                'entity_txt': entity,
            }

        if (model_enum, document_id) in double2anno:
            for exist_anno in double2anno[(model_enum, document_id)]:
                exist_start, exist_end, exist_mention, exist_entity = \
                    exist_anno['start'], exist_anno['end'], exist_anno['mention_txt'], exist_anno['entity_txt']

                if exist_start >= end_pos or exist_end <= start_pos:
                    continue
                else:
                    assert start_pos == exist_start
                    assert end_pos == exist_end
                    assert mention == exist_mention
                    assert entity == exist_entity

                    raise ValueError('overlapped annotation!', anno, exit_annot)

        double2anno[(model_enum, document_id)].append(anno)

    for key in double2anno:
        tmp_anno = double2anno[key]
        tmp_anno = sorted(tmp_anno, key=lambda x: (x['start'], x['end']))
        double2anno[key] = tmp_anno

    return double2anno


def collect_anno_id2anno_from_anno(ori_anno):
    anno_id2anno = dict()
    for (id, document_id, model_enum, mention, entity, start_pos, end_pos) in ori_anno:
        assert type(id) is int
        assert id not in anno_id2anno

        assert type(document_id) is str
        assert type(model_enum) is str
        assert type(mention) is str
        assert type(entity) is str
        assert type(start_pos) is int
        assert type(end_pos) is int

        anno_id2anno[id] = {
            'start': start_pos,
            'end': end_pos,
            'mention_txt': mention,
            'entity_txt': entity,
            # **YD** model_enum also needs to be assign
            'model_enum': model_enum,
        }

    return anno_id2anno


def collect_double2anno_from_verified_anno_and_anno_id2anno_from_anno(verified_anno, anno_id2anno):
    """
    mysql> describe verified_annotations;
    +-----------------+------------------+------+-----+---------+----------------+
    | Field           | Type             | Null | Key | Default | Extra          |
    +-----------------+------------------+------+-----+---------+----------------+
    | id              | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
    | document_id     | varchar(300)     | YES  |     | NULL    |                |
    | user_id         | varchar(200)     | YES  |     | NULL    |                |
    | model_enum      | varchar(200)     | YES  |     | NULL    |                |
    | annotation_id   | int(11)          | YES  |     | NULL    |                |
    | verified        | tinyint(1)       | YES  |     | NULL    |                |
    | mention         | varchar(200)     | YES  |     | NULL    |                |
    | modified_entity | varchar(200)     | YES  |     | NULL    |                |
    +-----------------+------------------+------+-----+---------+----------------+
    8 rows in set (0.00 sec)
    :param verified_anno:  list of tuples. (id, document_id, user_id, model_enum, annotation_id, verified, mention, modified_entity)
    :param anno_id2anno: anno_id2anno extracted from ori_anno (output of function "collect_anno_id2anno_from_anno")
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

    print('collecting verified annotations from DB list.')
    print(len(verified_anno), ' total annotations are collected, may include repeated annotations')
    double2anno = defaultdict(list)
    for (id, document_id, user_id, fake_model_enum, annotation_id, verified, mention, modified_entity) \
        in verified_anno:
        assert annotation_id in anno_id2anno
        anno = anno_id2anno[annotation_id]

        modified_entity = process_wiki_url(modified_entity)

        assert mention == anno['mention_txt']
        start_pos = anno['start']
        end_pos = anno['end']

        # **YD** the model_enum should come from the "anno_id2anno"
        model_enum = anno['model_enum']

        add_verified_anno = {
            'start': start_pos,
            'end': end_pos,
            'mention_txt': mention,
            'entity_txt': modified_entity,
        }

        find_flag = False
        if (model_enum, document_id) in double2anno:
            for exist_anno in double2anno[(model_enum, document_id)]:
                exist_start, exist_end, exist_mention, exist_entity = \
                    exist_anno['start'], exist_anno['end'], exist_anno['mention_txt'], exist_anno['entity_txt']

                if exist_start >= end_pos or exist_end <= start_pos:
                    continue
                else:
                    if start_pos != exist_start or end_pos != exist_end or mention != exist_mention or \
                            modified_entity != exist_entity:

                        raise ValueError('overlapped but not equal annotation!', anno, exit_annot)
                    find_flag = True

        if not find_flag:
            double2anno[(model_enum, document_id)].append(add_verified_anno)

    for key in double2anno:
        tmp_anno = double2anno[key]
        tmp_anno = sorted(tmp_anno, key=lambda x: (x['start'], x['end']))
        double2anno[key] = tmp_anno

    return double2anno
