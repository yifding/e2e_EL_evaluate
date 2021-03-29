import os
from collections import defaultdict

import stanza
from tqdm import tqdm

from e2e_EL_evaluate.utils.check_xml_anno import check_xml_anno
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml

# stanza.version == 1.2
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


def xml2stanza_token(
    prefix,
    dataset,
    output_prefix,
    allow_mention_without_entity=True,
):
    """
    This function inputs a 'xml EL annotation' directory with specified datatset, and outputs a stanza tokenized
    '.conll' EL file, similar to AIDA-CONLL EL dataset.

    :param prefix: input directory of '.xml EL annotation'
    :param dataset: a string represents a dataset name
    :param output_prefix: output directory

    :return: None
    """
    print('dataset', dataset, 'path', prefix, 'output_path', output_prefix)
    doc_name2txt, doc_name2anno = gen_anno_from_xml(
        prefix,
        dataset,
        allow_mention_without_entity=allow_mention_without_entity,
    )
    check_xml_anno(doc_name2txt, doc_name2anno)

    num_split = 0
    doc_name2tokens = defaultdict(list)

    for doc_name in tqdm(doc_name2txt):
        doc_anno = doc_name2anno[doc_name] if doc_name in doc_name2anno else []
        doc_txt = doc_name2txt[doc_name]

        doc_stanza_tokens = TOKENIZER(doc_txt).to_dict()
        store_list = []

        # edit list of list by indexing
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

    write_conll(output_prefix, dataset, doc_name2tokens)
    print('num_split', num_split)


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


def write_conll(prefix, dataset, doc_name2tokens):
    os.makedirs(prefix, exist_ok=True)
    out_file = os.path.join(prefix, dataset + '.conll')
    with open(out_file, 'w') as writer:
        for doc_name in sorted(doc_name2tokens.keys()):
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
