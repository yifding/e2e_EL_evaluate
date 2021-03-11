#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from collections import defaultdict


AIDA_TRAIN_FILE = "aida_train.txt"
AIDA_TEST_FILE = "testa_testb_aggregate_original"

UNKNOWN_ENTITY = 'NIL'
UNKNOWN_WIKI_ID = '0000'


def read_aida(aida_train_file="aida_train.txt"):
    text = ""
    redict = defaultdict(list)
    text_dict = dict()
    doc_name = "Unknown"
    num_doc = 0
    with open(aida_train_file, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith("-DOCSTART-"):
                if doc_name != "Unknown":
                    text_dict[doc_name] = text
                    text = ''

                assert line.startswith("-DOCSTART- (")
                assert line.endswith(")\n")

                doc_name = line[len("-DOCSTART- ("): -len(")\n")]
                doc_name = doc_name.replace(' ','_')
                num_doc += 1

            elif line == '\n':
                text += '\n'

            else:
                splits = line.rstrip('\n').split('\t')
                # len(splits) = [1, 4, 6, 7]
                # 1: single symbol
                # 4: ['Tim', 'B', "Tim O'Gorman", '--NME--']
                # 6: ['House', 'B', 'House of Commons', 'House_of_Commons', 'http://en.wikipedia.org/wiki/House_of_Commons', '216091']
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

        if doc_name not in text_dict:
            text_dict[doc_name] = text

    return text_dict, redict


def write_xml(dataset, xml_file, redict):
    print('ready to write:', 'dataset', dataset, 'path', xml_file)

    with open(xml_file, 'w') as writer:
        writer.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
        writer.write('<' + dataset + '.entityAnnotation>' + '\n')
        for document in redict:
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


def check(dataset, text_dict, redict):
    print('CHECK the correctness of transforming dataset: ', dataset)
    num_ner = 0
    num_el = 0

    for doc_name in redict:
        assert doc_name in text_dict
        document = text_dict[doc_name]

        for anno in redict[doc_name]:
            entity_txt = anno['entity_txt']
            mention_txt = anno['mention_txt']
            start = anno['start']
            end = anno['end']

            GT_mention = document[start:end]

            if not GT_mention == mention_txt:
                print('GT_mention', GT_mention)
                print('mention_txt', mention_txt)

            assert len(GT_mention) == len(mention_txt)
            assert GT_mention == mention_txt

            if entity_txt == UNKNOWN_ENTITY:
                num_ner += 1
            else:
                num_el += 1

    print('num_ner: ', num_ner, 'num_el: ', num_el)


def process_aida_train(args):
    aida_train_file = os.path.join(args.input_dir, AIDA_TRAIN_FILE)
    text_dict_train, redict_train = read_aida(aida_train_file)
    check('aida_train', text_dict_train, redict_train)

    aida_train_folder = os.path.join(args.output_dir, 'aida_train/RawText')
    os.makedirs(aida_train_folder, exist_ok=True)
    aida_train_xml = os.path.join(args.output_dir, 'aida_train/aida_train.xml')
    write_xml('aida_train', aida_train_xml, redict_train)

    for doc_name in text_dict_train:
        file_name = os.path.join(aida_train_folder, doc_name)
        with open(file_name, 'w') as writer:
            writer.write(text_dict_train[doc_name])


def process_aida_test(args):
    aida_test_file = os.path.join(args.input_dir, AIDA_TEST_FILE)
    text_dict, redict = read_aida(aida_test_file)

    text_dict_testa = dict()
    text_dict_testb = dict()

    redict_testa = dict()
    redict_testb = dict()

    for doc_name in text_dict:
        if 'testa' in doc_name:
            text_dict_testa[doc_name] = text_dict[doc_name]
        elif 'testb' in doc_name:
            text_dict_testb[doc_name] = text_dict[doc_name]
        else:
            raise ValueError("unknown document")

    for doc_name in redict:
        if 'testa' in doc_name:
            redict_testa[doc_name] = redict[doc_name]
        elif 'testb' in doc_name:
            redict_testb[doc_name] = redict[doc_name]
        else:
            raise ValueError("unknown document")

    check('aida_testa', text_dict_testa, redict_testa)
    check('aida_testb', text_dict_testb, redict_testb)

    # write aida_testa

    aida_testa_folder = os.path.join(args.output_dir, 'aida_testa/RawText')
    os.makedirs(aida_testa_folder, exist_ok=True)
    aida_testa_xml = os.path.join(args.output_dir, 'aida_testa/aida_testa.xml')
    write_xml('aida_testa', aida_testa_xml, redict_testa)

    for doc_name in text_dict_testa:
        file_name = os.path.join(aida_testa_folder, doc_name)
        with open(file_name, 'w') as writer:
            writer.write(text_dict_testa[doc_name])

    # write aida_testb
    aida_testb_folder = os.path.join(args.output_dir, 'aida_testb/RawText')
    os.makedirs(aida_testb_folder, exist_ok=True)
    aida_testb_xml = os.path.join(args.output_dir, 'aida_testb/aida_testb.xml')
    write_xml('aida_testb', aida_testb_xml, redict_testb)

    for doc_name in text_dict_testb:
        file_name = os.path.join(aida_testb_folder, doc_name)
        with open(file_name, 'w') as writer:
            writer.write(text_dict_testb[doc_name])


def main(args):
    print('input directory: ', args.input_dir, 'output dir: ', args.output_dir)
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    process_aida_train(args)
    process_aida_test(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/EL_resource/data/raw/AIDA-CONLL/',
        help='Specify the input AIDA directory',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/processed/AIDA-CONLL/ori2xml',
        help='Specify the input AIDA directory',
    )
    args = parser.parse_args()
    main(args)