# We conduct experiments on Mturk on entity disambiguation only.
# Give a annotated documents, people can
# 1. verify the (mention, entity) annotation pair.
# 2. remove the (mention, entity) annotation pair.
# 3. change the entity of (mention, entity) annotation pair.

# this file is to count those 3 different numbers given two "xml" processed annotation.

# anno = {
#   'testa_1001': [
#       {'start': , 'end', 'mention_txt': , 'entity_txt': ,
#        }
#   ]
# }


class EditEntityCount(object):
    def __init__(self, verify, remove, edit):
        self.verify = verify
        self.remove = remove
        self.edit = edit


def edit_entity_from_xml(doc_name2txt, model_doc_name2anno, GT_doc_name2anno):
    """
    the mention of annotations in model_doc_name2anno must present in GT_doc_name2anno
    :param doc_name2txt:
    :param model_doc_name2anno:
    :param GT_doc_name2anno:
    :return:
    """
    for doc_name in model_doc_name2anno:
        assert doc_name in doc_name2txt

    for doc_name in GT_doc_name2anno:
        assert doc_name in doc_name2txt

    fake_verify = 0
    verify = remove = edit = 0
    for doc_name in model_doc_name2anno:
        assert doc_name in GT_doc_name2anno
        for anno in model_doc_name2anno[doc_name]:
            FIND_FLAG = False
            for GT_anno in GT_doc_name2anno[doc_name]:
                if anno['start'] == GT_anno['start']:
                    FIND_FLAG = True
                    assert anno['end'] == GT_anno['end']
                    assert anno['mention_txt'] == GT_anno['mention_txt']
                    if anno['entity_txt'] == GT_anno['entity_txt']:
                        verify += 1
                    break
            assert FIND_FLAG

    for doc_name in GT_doc_name2anno:
        for anno in GT_doc_name2anno[doc_name]:
            if doc_name not in model_doc_name2anno:
                remove += 1
            else:
                FIND_FLAG = False
                for model_anno in model_doc_name2anno[doc_name]:
                    if anno['start'] == model_anno['start']:
                        FIND_FLAG = True
                        assert anno['end'] == model_anno['end']
                        assert anno['mention_txt'] == model_anno['mention_txt']
                        if anno['entity_txt'] == model_anno['entity_txt']:
                            fake_verify += 1
                        else:
                            edit += 1
                        break
                if not FIND_FLAG:
                    remove += 1

    assert verify == fake_verify

    edit_entity_count = EditEntityCount(verify, remove, edit)
    return edit_entity_count
