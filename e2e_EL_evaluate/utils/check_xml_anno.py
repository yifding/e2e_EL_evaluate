UNKNOWN_ENTITY_LIST = ['NIL', '']


def check_xml_anno(text_dict, redict):
    num_el = 0
    num_ner = 0

    for doc_name in redict:
        assert doc_name in text_dict
        document = text_dict[doc_name]

        for anno in redict[doc_name]:
            entity_txt = anno['entity_txt']
            mention_txt = anno['mention_txt']
            start = anno['start']
            end = anno['end']

            GT_mention = document[start:end]

            if GT_mention != mention_txt:
                print('GT_mention', GT_mention)
                print('mention_txt', mention_txt)

            assert len(GT_mention) == len(mention_txt)
            assert GT_mention == mention_txt

            if entity_txt in UNKNOWN_ENTITY_LIST:
                num_ner += 1
            else:
                num_el += 1

    print('num_ner: ', num_ner, 'num_el: ', num_el)
