import os
import argparse
from urllib.parse import quote
from collections import defaultdict

import stanza
from tqdm import tqdm

from gen_anno_from_xml import gen_anno_from_xml


TOKENIZER = stanza.Pipeline(lang='en', processors='tokenize')

"""
# OUTPUT of TOKENIZER, is a list of list, outer list is by sentence, inner list is by token.
# cut the inner list by adding extra tokens (changing the list by inserting more elements of slices)
doc = TOKENIZER('SOME DOCUMENTATION').to_dict()
[
    [
        {'id': 1, 'text': 'Kevorkian', 'misc': 'start_char=0|end_char=9'}, 
        {'id': 2, 'text': 'attends', 'misc': 'start_char=10|end_char=17'}, 
        {'id': 3, 'text': 'third', 'misc': 'start_char=18|end_char=23'}, 
        {'id': 4, 'text': 'suicide', 'misc': 'start_char=24|end_char=31'}, 
    ], 
    [
        {'id': 1, 'text': 'in', 'misc': 'start_char=32|end_char=34'}, 
        {'id': 2, 'text': 'week', 'misc': 'start_char=35|end_char=39'}, 
        {'id': 3, 'text': '.', 'misc': 'start_char=39|end_char=40'}
    ],
]
"""


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


def catch_start_end(s):
    """
    input string is like: "start_char=2|end_char=8"
    """
    parts = s.split("|")
    assert len(parts) == 2
    start_char = "start_char="
    end_char = "end_char="
    pre, post = parts[0], parts[1]
    assert pre.startswith(start_char)
    assert post.startswith(end_char)
    start = int(pre[len(start_char):])
    end = int(post[len(end_char):])

    return start, end


def doc_name_rank(s):
    if 'testa' in s:
        splits = s.split('testa')
        return int(splits[0])
    elif 'testb' in s:
        splits = s.split('testb')
        return int(splits[0])
    else:
        assert '_' in s
        splits = s.split('_')
        assert len(splits) == 2
        return int(splits[0])


def check_annotations(args):
    for data_name in args.data_names:
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, data_name)
        for doc_name in doc_name2anno:
            assert doc_name in doc_name2txt
            doc_txt = doc_name2txt[doc_name]
            doc_anno = doc_name2anno[doc_name]
            for anno in doc_anno:
                start, end, mention_txt, entity_txt = \
                    anno['start'], anno['end'], anno['mention_txt'], anno['entity_txt']
                assert end - start == len(mention_txt)
                assert doc_txt[start: end] == mention_txt


def gen_token_el(store_token, doc_anno):
    text, misc = store_token['text'], store_token['misc']
    token_start, token_end = catch_start_end(misc)
    find_mention = False
    ans = Token(text=text, start=token_start, end=token_end, mention='', entity='')
    # more than one mention found is INVALID
    # inside token label is INVALID
    for anno in doc_anno:
        start, end, mention_txt, entity_txt = anno['start'], anno['end'], anno['mention_txt'], anno['entity_txt']
        if token_start < start < token_end or token_start < end < token_end:
            raise ValueError('inside token label!')
        if start <= token_start and token_end <= end:
            if find_mention:
                raise ValueError('more than one mention found!')
            find_mention = True
            ans = Token(text=text, start=token_start, end=token_end, mention=mention_txt, entity=entity_txt)

    return ans


def gen_ele(stanza_token, doc_anno):
    ans = []
    indices = set()
    token = stanza_token['text']
    assert len(token) >= 1
    misc = stanza_token['misc']

    indices.add(0)
    indices.add(len(token))

    token_start, token_end = catch_start_end(misc)
    for anno in doc_anno:
        start, end, mention_text, entity_txt = anno['start'], anno['end'], anno['mention_txt'], anno['entity_txt']
        if token_start < start <= token_end - 1:
            indices.add(start - token_start)
        if token_start < end <= token_end - 1:
            indices.add(end - token_start)

    indices = sorted(indices)
    for i in range(len(indices) - 1):
        tmp_start, tmp_end = indices[i], indices[i+1]
        assert 0 < tmp_end - tmp_start <= len(token)
        atom = {
            'text': token[tmp_start: tmp_end],
            'misc': 'start_char={}|end_char={}'.format(tmp_start + token_start, tmp_end + token_start)
        }
        ans.append(atom)

    return ans


def write_conll(args, data_name, doc_name2tokens):
    out_file = os.path.join(args.output_dir, data_name + '.conll')
    with open(out_file, 'w') as writer:
        for doc_name in sorted(doc_name2tokens.keys(), key=doc_name_rank):
            doc_name = doc_name.replace(' ', '_').replace('&amp;', '&')
            writer.write('-DOCSTART- (' + doc_name + ')' + '\n')
            for doc_name2token_sentence in doc_name2tokens[doc_name]:
                pre_mention = None
                for token in doc_name2token_sentence:
                    writer.write(token.text)
                    writer.write('\t')
                    writer.write(str(token.start))
                    writer.write('\t')
                    writer.write(str(token.end))
                    if token.mention != '':
                        if token.mention != pre_mention:
                            writer.write('\t')
                            writer.write('B')
                            pre_mention = token.mention
                        else:
                            writer.write('\t')
                            writer.write('I')

                        writer.write('\t')
                        writer.write(token.mention)
                        writer.write('\t')
                        writer.write(token.entity)
                    writer.write('\n')
                writer.write('\n')


def tokenize(args):
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    # check annotations
    check_annotations(args)

    for data_name in args.data_names:
        print('dataset: ', data_name)

        num_split = 0

        doc_name2tokens = defaultdict(list)
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, data_name)

        for doc_name in tqdm(doc_name2txt):
            doc_anno = doc_name2anno[doc_name] if doc_name in doc_name2anno else []
            doc_txt = doc_name2txt[doc_name]

            doc_stanza_tokens = TOKENIZER(doc_name2txt[doc_name]).to_dict()
            store_list = []

            # edit list of list by indexing
            # **YD** See line 13 for tokenized examples
            for doc_stanza_token in doc_stanza_tokens:
                store_list.append([])
                for stanza_token in doc_stanza_token:
                    ele = gen_ele(stanza_token, doc_anno)
                    num_split += len(ele) - 1
                    store_list[-1].extend(ele)

            for store_sentence in store_list:
                doc_name2tokens[doc_name].append([])
                for store_token in store_sentence:
                    token_label = gen_token_el(store_token, doc_anno)
                    doc_name2tokens[doc_name][-1].append(token_label)

        write_conll(args, data_name, doc_name2tokens)
        print('num_split', num_split)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/processed/AIDA-CONLL/ori2xml",
        type=str,
    )

    parser.add_argument(
        "--output_dir",
        default="/scratch365/yding4/e2e_EL_evaluate/data/processed/AIDA-CONLL/transform_xml2stanza_token/",
        type=str,
    )

    parser.add_argument(
        "--data_names",
        default="['aida_train', 'aida_testa', 'aida_testb']",
        type=eval,
    )

    args = parser.parse_args()
    tokenize(args)