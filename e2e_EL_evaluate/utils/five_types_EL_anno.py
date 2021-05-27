# 	a. Same mention, same entity
# 	b. Same mention, different.
# 	c. at least one overlapped mention with same entity.
# 	d. at least one overlapped mention, all the overlapped mentions having different entities.
# 	e. Only in model, not in template.


def five_types_EL_anno(model_doc_name2anno, template_doc_name2anno):
    type_a, type_b, type_c, type_d, type_e = 0, 0, 0, 0, 0
    for doc_name in model_doc_name2anno:
        for anno in model_doc_name2anno[doc_name]:
            start, end, mention_txt, entity_txt = \
                anno['start'], anno['end'], anno['mention_txt'], anno['entity_txt']
            find_a, find_b, find_c, find_d, find_e = False, False, False, False, False
            if doc_name not in template_doc_name2anno:
                type_e += 1
            else:
                for template_anno in template_doc_name2anno[doc_name]:
                    tmp_start, tmp_end, tmp_mention_txt, tmp_entity_txt = \
                        template_anno['start'], template_anno['end'], template_anno['mention_txt'], template_anno['entity_txt']

                    if start == tmp_start and end == tmp_end:
                        if entity_txt == tmp_entity_txt:
                            find_a = True
                        else:
                            print('doc_name: ', doc_name)
                            print('anno: ', anno)
                            print('tmp_anno: ', template_anno)
                            find_b = True

                    elif start <= tmp_start < end or tmp_start <= start < tmp_end:
                        if entity_txt == tmp_entity_txt:
                            find_c = True
                        else:
                            find_d = True

                if find_a:
                    type_a += 1
                elif find_b:
                    type_b += 1
                elif find_c:
                    type_c += 1
                elif find_d:
                    type_d += 1
                else:
                    type_e += 1

    stat = {
        'type_a': type_a,
        'type_b': type_b,
        'type_c': type_c,
        'type_d': type_d,
        'type_e': type_e,
    }

    return stat
