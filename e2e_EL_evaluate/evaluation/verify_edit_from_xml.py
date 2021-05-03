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
    for index, doc_name in enumerate(doc_name2txt):
        assert doc_name in model_doc_name2anno
        assert doc_name in GT_doc_name2anno

        if not len(model_doc_name2anno[doc_name]) == len(GT_doc_name2anno[doc_name]):
            print('index', index, 'doc_name', doc_name)
            print('doc_name2txt[doc_name]', doc_name2txt[doc_name])
            print('GT_doc_name2anno[doc_name]', GT_doc_name2anno[doc_name])
        assert len(model_doc_name2anno[doc_name]) == len(GT_doc_name2anno[doc_name])

    verify = remove = edit = 0
    for doc_name in doc_name2txt:
        for model_anno, GT_anno in zip(model_doc_name2anno[doc_name], GT_doc_name2anno[doc_name]):
            assert model_anno['start'] == GT_anno['start']
            assert model_anno['end'] == GT_anno['end']
            assert model_anno['mention_txt'] == GT_anno['mention_txt']
            assert GT_anno['entity_txt'] != ''
            if model_anno['entity_txt'] == GT_anno['entity_txt']:
                verify += 1
            elif model_anno['entity_txt'] == '':
                remove += 1
            else:
                edit += 1

    edit_entity_count = EditEntityCount(verify, remove, edit)
    return edit_entity_count
