import os
from collections import defaultdict


def gen_anno_from_xml(
        prefix,
        dataset,
        allow_mention_shift=False,
        allow_mention_without_entity=False,
        allow_repeat_annotation=False,
    ):

    """
    this function reads a standard xml EL annotation with its documents
    {dataset}:
    |
    |--RawText:
    |      |
    |      |---{doc_name} (with the txts)
    |
    |--{dataset}.xml (annotation of all the {doc_name})

    ATTENTION:
        a. the '&' is replaced as '&amp;' in both "txt" and "annotation" reading. '&' is not allowed in '.xml' file
        b. in the '.xml' annotation, 'doc_name' has no ' ', it has '_' instead. In mention and entity annotation, it has
        no '_' but has ' ' instead.

    :param prefix: the absolute path before the dataset directory.

    :param dataset: name of a dataset. It also forms the name of '.xml'.

    :param allow_mention_shift: allow mismatch between "txt[offset: offset + length]" and "{annotated mention}".
    If the flag is set to True: it will uses the length of "{annotated mention}" as actual length. Search the mention
    from "offset" - 10 to "offset + 100" to find this mention.
    If the flag is set to False: it will raise ERROR if a mismatch is found.

    :param allow_mention_without_entity: allow empty entity annotation, either '' or 'NIL', called "NER annotation".
    If the flag is set to True: the empty annotation will preserve, the entity will change to ''.
    If the flag is set to False: raise ERROR if an empty entity is found.

    :param allow_repeat_annotation: allow repeated annotation.
    If the flag is set to True: repeated annotation will not be considered as outputs
    If the flag is set to False: raise ERROR if a repeat annotation is found.

    :return:
    doc_name2txt, doc_name2anno:
    doc_name2txt is a dictionary of string. Each doc_name corresponds to a documentation of a dataset.
    doc_name2anno is a dictionary of list. Each doc_name corresponds to a documentation of a dataset.
    each element(ele) in the list is a dictionary formed with four elements:

    ele = {
            'start': offset,    # starting position of the mention in the doc_name txt.
            'end': offset + length, # endding position of the mention in the doc_name txt.
            'mention_txt': cur_mention, # annotated mention.
            'entity_txt': cur_ent_title, # annotated entity. '' or 'NIL' represents empty entity annotation (NER).
        }
    """

    raw_text_prefix = os.path.join(prefix, dataset + '/' + 'RawText')
    xml_file = os.path.join(prefix, dataset + '/' + dataset + '.xml')
    doc_names = os.listdir(raw_text_prefix)

    # collect documentation for each doc_name
    doc_name2txt = dict()

    for doc_name in doc_names:
        txt_path = os.path.join(raw_text_prefix, doc_name)
        txt = ''
        with open(txt_path, 'r') as reader:
            for line in reader:
                txt += line
        doc_name2txt[doc_name] = txt.replace('&amp;', '&')

    # collect mention/entity annotation from xml
    doc_name2anno = defaultdict(list)
    # nested named entity recognition problem in silver + gold
    reader = open(xml_file, 'r')

    doc_str_start = 'document docName=\"'
    doc_str_end = '\">'

    line = reader.readline()
    num_el_anno = 0
    num_ner_anno = 0
    num_shift_anno = 0
    num_change_length = 0
    cur_doc_name = ''

    while line:
        if doc_str_start in line:
            start = line.find(doc_str_start)
            end = line.find(doc_str_end)
            cur_doc_name = line[start + len(doc_str_start): end]
            cur_doc_name = cur_doc_name.replace('&amp;', '&').replace(' ', '_')
            assert cur_doc_name in doc_name2txt

        else:
            if '<annotation>' in line:
                line = reader.readline()
                assert '<mention>' in line and '</mention>' in line

                m_start = line.find('<mention>') + len('<mention>')
                m_end = line.find('</mention>')

                cur_mention = line[m_start: m_end]
                cur_mention = cur_mention.replace('&amp;', '&').replace('_', ' ')

                line = reader.readline()
                # assert '<wikiName>' in line and '</wikiName>' in line
                e_start = line.find('<wikiName>') + len('<wikiName>')
                e_end = line.find('</wikiName>')
                cur_ent_title = '' if '<wikiName/>' in line else line[e_start: e_end]
                cur_ent_title.replace('&amp;', '&').replace('_', ' ')

                line = reader.readline()
                assert '<offset>' in line and '</offset>' in line
                off_start = line.find('<offset>') + len('<offset>')
                off_end = line.find('</offset>')
                offset = int(line[off_start: off_end])

                line = reader.readline()
                assert '<length>' in line and '</length>' in line
                len_start = line.find('<length>') + len('<length>')
                len_end = line.find('</length>')
                length_record = int(line[len_start: len_end])
                length = len(cur_mention)

                if length != length_record:
                    print('mention', cur_mention, 'offset', offset, 'length', length, 'length_record', length_record)
                    num_change_length += 1

                line = reader.readline()
                if '<entity/>' in line:
                    line = reader.readline()

                assert '</annotation>' in line

                # if cur_ent_title != 'NIL' and cur_ent_title != '':
                assert cur_doc_name != ''
                ele = {
                        'start': offset,
                        'end': offset + length,
                        'mention_txt': cur_mention,
                        'entity_txt': cur_ent_title,
                    }

                doc_txt = doc_name2txt[cur_doc_name]
                pos_mention = doc_txt[offset: offset + length]

                if allow_mention_shift:
                    if pos_mention != ele['mention_txt']:
                        num_shift_anno += 1
                        offset = max(0, offset - 10)
                        while pos_mention != cur_mention:
                            offset = offset + 1
                            pos_mention = doc_txt[offset: offset + length]
                            if offset > ele['start'] + 100:
                                print('pos_mention', doc_txt[anno['offset']: anno['offset'] + length], anno['mention_txt'])
                                raise ValueError('huge error!')
                        ele['start'] = offset
                        ele['end'] = offset + length
                else:
                    if pos_mention != ele['mention_txt']:
                        print('pos_mention', pos_mention)
                        print("ele['mention_txt']", ele['mention_txt'])
                    assert pos_mention == ele['mention_txt'], 'Unmatched mention between annotation mention ' \
                                                              'and annotation position'

                # allow_mention_without_entity
                if ele['entity_txt'] == '' or ele['entity_txt'] == 'NIL':
                    ele['entity_txt'] = ''

                # consider repeat annotations in wikipedia
                if ele not in doc_name2anno[cur_doc_name]:
                    if ele['entity_txt'] != '':
                        doc_name2anno[cur_doc_name].append(ele)
                        num_el_anno += 1
                    else:
                        num_ner_anno += 1
                        if allow_mention_without_entity:
                            doc_name2anno[cur_doc_name].append(ele)
                else:
                    if not allow_repeat_annotation:
                        raise ValueError('find repeated annotation: ' + str(ele))

        line = reader.readline()

    print(
        'num_ner_anno', num_ner_anno,
        'num_el_anno', num_el_anno,
        'num_shift_anno', num_shift_anno,
        'num_change_length', num_change_length
    )

    # **YD** post-processing: sort the annotation by start and end.
    for doc_name in doc_name2anno:
        tmp_anno = doc_name2anno[doc_name]
        tmp_anno = sorted(tmp_anno, key=lambda x: (x['start'], x['end']))
        doc_name2anno[doc_name] = tmp_anno

    return doc_name2txt, doc_name2anno
