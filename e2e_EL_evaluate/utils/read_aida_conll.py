from collections import defaultdict

from e2e_EL_evaluate.utils.check_xml_anno import check_xml_anno

UNKNOWN_ENTITY = ''
UNKNOWN_WIKI_ID = '0000'
AIDA_TRAIN_FILE = "aida_train.txt"
AIDA_TEST_FILE = "testa_testb_aggregate_original"


def read_aida_conll(aida_file):
    """
    Standard reading function for original aida-conll-2003 dataset. This aims for EL version, it has more well-known and
    standard format of NER dataset.

    :param aida_file: input file of AIDA_TRAIN_FILE or AIDA_TEST_FILE.
    :return: text_dict, redict
    text_dict: doc_name to txt.
    redict:
    """
    assert aida_file.endswith(AIDA_TRAIN_FILE) or aida_file.endswith(AIDA_TEST_FILE)
    text = ""
    redict = defaultdict(list)
    text_dict = dict()
    doc_name = "Unknown"
    num_doc = 0

    with open(aida_file, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith("-DOCSTART-"):
                if doc_name != "Unknown":
                    text_dict[doc_name] = text
                    text = ''

                assert line.startswith("-DOCSTART- (")
                assert line.endswith(")\n")

                doc_name = line[len("-DOCSTART- ("): -len(")\n")]
                doc_name = doc_name.replace(' ', '_')
                num_doc += 1

            elif line == '\n':
                text += '\n'

            else:
                splits = line.rstrip('\n').split('\t')
                # len(splits) = [1, 4, 6, 7]
                # 1: single symbol
                # 4: ['Tim', 'B', "Tim O'Gorman", '--NME--']
                # 6: ['House', 'B', 'House of Commons',
                # 'House_of_Commons', 'http://en.wikipedia.org/wiki/House_of_Commons', '216091']
                # 7: ['German', 'B', 'German', 'Germany', 'http://en.wikipedia.org/wiki/Germany', '11867', '/m/0345h']

                len_row = len(splits)
                assert len_row in [1, 4, 6, 7]
                if len_row == 6 or len_row == 7:
                    sign = splits[1]
                    if sign == 'B':
                        splits[3] = splits[3].encode().decode("unicode-escape")

                        mention_txt = splits[2]
                        entity_txt = splits[3]
                        entity_txt = entity_txt.replace('_', ' ')
                        tmp_wiki_split = splits[4].split('/wiki/')
                        wiki_id = splits[5]

                        assert len(tmp_wiki_split) == 2
                        if not entity_txt == tmp_wiki_split[1].replace('_', ' '):
                            print('line_name', i)
                            print('entity_txt', entity_txt)
                            print('wikipedia_name', tmp_wiki_split[1].replace('_', ' '))
                        assert entity_txt == tmp_wiki_split[1].replace('_', ' ')

                        if splits[0] == ',' or splits[0] == '.' or splits[0] == '\'s' \
                                or splits[0] == ':' or splits[0] == '!':
                            start = len(text)
                        else:
                            if text == '' or text[-1] == '\n':
                                start = len(text)
                            else:
                                start = len(text) + 1

                        end = start + len(mention_txt)

                        cur_m_e_dict = {
                            'start': start,
                            'end': end,
                            'mention_txt': mention_txt,
                            'entity_txt': entity_txt,
                            'wiki_id': wiki_id,
                        }

                        redict[doc_name].append(cur_m_e_dict)

                elif len_row == 4:
                    sign = splits[1]
                    if sign == 'B':
                        mention_txt = splits[2]

                        if splits[0] == ',' or splits[0] == '.' or splits[0] == '\'s' \
                                or splits[0] == ':' or splits[0] == '!':
                            start = len(text)
                        else:
                            if text == '' or text[-1] == '\n':
                                start = len(text)
                            else:
                                start = len(text) + 1

                        end = start + len(mention_txt)
                        cur_m_e_dict = {
                            'start': start,
                            'end': end,
                            'mention_txt': mention_txt,
                            'entity_txt': UNKNOWN_ENTITY,
                            'wiki_id': UNKNOWN_WIKI_ID,
                        }

                        redict[doc_name].append(cur_m_e_dict)

                if splits[0] == ',' or splits[0] == '.' or splits[0] == '\'s' or splits[0] == ':' or splits[0] == '!':
                    text += splits[0]
                else:
                    if text == '' or text[-1] == '\n':
                        text += splits[0]
                    else:
                        text += ' ' + splits[0]

        # **YD** add potentially the last left doc_name.
        if doc_name not in text_dict:
            text_dict[doc_name] = text

    # **YD** post-processing: sort the annotation by start and end.
    for doc_name in redict:
        tmp_anno = redict[doc_name]
        tmp_anno = sorted(tmp_anno, key=lambda x: (x['start'], x['end']))
        redict[doc_name] = tmp_anno

    # **YD** post-processing: check the correctness of the loading outputs
    check_xml_anno(text_dict, redict)

    return text_dict, redict

