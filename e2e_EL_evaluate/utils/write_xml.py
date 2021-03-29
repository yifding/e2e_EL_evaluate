import os


def write_xml(prefix, dataset, doc_name2txt, doc_name2anno):
    """
    this function writes a standard xml EL annotation with its documents

    {dataset}:
    |
    |--RawText:
    |      |
    |      |---{doc_name} (with the txts)
    |
    |--{dataset}.xml (annotation of all the {doc_name})

    :param prefix: directory path to the writing destination
    :param dataset: name of a dataset
    :param doc_name2txt: a dictionary of string. Each doc_name corresponds to a documentation of a dataset.
    :param doc_name2anno: a dictionary of list. Each doc_name corresponds to a documentation of a dataset.

    each element(ele) in the list is a dictionary formed with four elements:
    ele = {
            'start': offset,    # starting position of the mention in the doc_name txt.
            'end': offset + length, # endding position of the mention in the doc_name txt.
            'mention_txt': cur_mention, # annotated mention.
            'entity_txt': cur_ent_title, # annotated entity. '' or 'NIL' represents empty entity annotation (NER).
        }
    :return: None
    """
    print('ready to write xml EL annotation:', 'dataset', dataset, 'path', prefix)
    dataset_prefix = os.path.join(prefix, dataset)
    os.makedirs(dataset_prefix, exist_ok=True)

    write_annotation(prefix, dataset, doc_name2anno)
    write_txt(prefix, dataset, doc_name2txt)


def write_annotation(prefix, dataset, doc_name2anno):
    xml_file = os.path.join(prefix, dataset + '/' + dataset + '.xml')
    with open(xml_file, 'w') as writer:
        writer.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
        writer.write('<' + dataset + '.entityAnnotation>' + '\n')
        for document in sorted(doc_name2anno.keys()):
            anno_list = doc_name2anno[document]
            document = document.replace(' ', '_').replace('&', '&amp;')

            # <document docName="20001115_AFP_ARB.0093.eng">
            writer.write('\t' + '<document docName="' + document + '">' + '\n')
            for anno in anno_list:
                # a preparation
                mention_txt = anno['mention_txt']
                entity_txt = anno['entity_txt']
                start = anno['start']
                end = anno['end']

                mention_txt = mention_txt.replace('_', ' ').replace('&', '&amp;')
                entity_txt = entity_txt.replace('_', ' ').replace('&', '&amp;')

                # b write things down
                writer.write('\t\t' + '<annotation>' + '\n')

                writer.write('\t\t\t' + '<mention>' + mention_txt + '</mention>' + '\n')
                writer.write('\t\t\t' + '<wikiName>' + entity_txt + '</wikiName>' + '\n')
                writer.write('\t\t\t' + '<offset>' + str(start) + '</offset>' + '\n')
                writer.write('\t\t\t' + '<length>' + str(end - start) + '</length>' + '\n')

                writer.write('\t\t' + '</annotation>' + '\n')

            writer.write('\t' + '</document>' + '\n')
        writer.write('</' + dataset + '.entityAnnotation>' + '\n')


def write_txt(prefix, dataset, doc_name2txt):
    raw_text_prefix = os.path.join(prefix, dataset + '/' + 'RawText')
    os.makedirs(raw_text_prefix, exist_ok=True)
    for doc_name in doc_name2txt:
        file_name = os.path.join(raw_text_prefix, doc_name)
        with open(file_name, 'w') as writer:
            writer.write(doc_name2txt[doc_name])

