import os
from collections import defaultdict


def gen_anno_from_xml(prefix, dataset):
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
    cur_doc_name = ''

    while line:
        if doc_str_start in line:
            start = line.find(doc_str_start)
            end = line.find(doc_str_end)
            cur_doc_name = line[start + len(doc_str_start): end]
            cur_doc_name = cur_doc_name.replace('&amp;', '&')
            assert cur_doc_name in doc_name2txt

        else:
            if '<annotation>' in line:
                line = reader.readline()
                assert '<mention>' in line and '</mention>' in line

                m_start = line.find('<mention>') + len('<mention>')
                m_end = line.find('</mention>')

                cur_mention = line[m_start: m_end]
                cur_mention = cur_mention.replace('&amp;', '&')

                line = reader.readline()
                # assert '<wikiName>' in line and '</wikiName>' in line
                e_start = line.find('<wikiName>') + len('<wikiName>')
                e_end = line.find('</wikiName>')
                cur_ent_title = '' if '<wikiName/>' in line else line[e_start: e_end]

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

                assert length == length_record

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

                if cur_ent_title != 'NIL' and cur_ent_title != '':
                    num_el_anno += 1
                else:
                    num_ner_anno += 1

                doc_name2anno[cur_doc_name].append(ele)
        line = reader.readline()

    print('num_ner_anno', num_ner_anno, 'num_el_anno', num_el_anno)

    return doc_name2txt, doc_name2anno