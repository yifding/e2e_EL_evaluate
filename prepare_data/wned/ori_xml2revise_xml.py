import os
import argparse
from urllib.parse import quote
from collections import defaultdict

from tqdm import tqdm

from gen_anno_from_ori_xml import gen_anno_from_xml


class Token(object):
    def __init__(self, text, start, end, mention='', entity=''):
        self.text = text
        self.start = start
        self.end = end

        self.mention = mention
        self.entity = entity

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "'text': " + self.text \
            + " 'start': " + str(self.start) \
            + " 'end': " + str(self.end) \
            + " 'mention': " + str(self.mention) \
            + " 'entity': " + str(self.entity)


def write_xml(dataset, xml_file, redict):
    print('ready to write:', 'dataset', dataset, 'path', xml_file)

    with open(xml_file, 'w') as writer:
        writer.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
        writer.write('<' + dataset + '.entityAnnotation>' + '\n')
        for document in sorted(redict.keys()):
            tmps = redict[document]
            document = document.replace(' ', '_').replace('&', '&amp;')

            # <document docName="20001115_AFP_ARB.0093.eng">
            writer.write('\t' + '<document docName="' + document + '">' + '\n')
            for anno in tmps:
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


def process_wned(args):
    prefix = args.input_dir
    data_names = args.data_names
    output_prefix = args.output_dir
    os.makedirs(output_prefix, exist_ok=True)

    # check the annotation
    for data_name in data_names:
        print('start to check the dataset: ', data_name)
        doc_name2txt, doc_name2anno = gen_anno_from_xml(prefix, data_name)
        for doc_name in doc_name2anno:
            assert doc_name in doc_name2txt
            doc_txt = doc_name2txt[doc_name]
            doc_anno = doc_name2anno[doc_name]
            for anno in doc_anno:
                start, end, mention_txt, entity_txt = \
                    anno['start'], anno['end'], anno['mention_txt'], anno['entity_txt']
                assert end - start == len(mention_txt)
                assert doc_txt[start: end] == mention_txt
        print('check the dataset: ', data_name, 'successfully')

    for data_name in data_names:
        print('start to process dataset:', data_name)
        doc_name2txt, doc_name2anno = gen_anno_from_xml(prefix, data_name)
        xml_file = os.path.join(args.output_dir, data_name + '/' + data_name + '.xml')
        txt_dir = os.path.join(args.output_dir, data_name + '/RawText')
        os.makedirs(txt_dir, exist_ok=True)

        # **YD** sort the annotations by start first, and end second.
        for doc_name in doc_name2anno:
            tmp = doc_name2anno[doc_name]
            tmp = sorted(tmp, key=lambda x: x['end'])
            tmp = sorted(tmp, key=lambda x: x['start'])
            doc_name2anno[doc_name] = list(tmp)

            txt_file = os.path.join(txt_dir, doc_name)
            with open(txt_file, 'w') as writer:
                writer.write(doc_name2txt[doc_name])

        write_xml(data_name, xml_file, doc_name2anno)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        default="/scratch365/yding4/EL_resource/data/raw/wned-datasets/",
        type=str,
    )

    parser.add_argument(
        "--output_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/processed/wned/ori_xml2revise_xml",
        type=str,
    )

    parser.add_argument(
        "--data_names",
        default="['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia']",
        type=eval,
    )

    args = parser.parse_args()
    process_wned(args)