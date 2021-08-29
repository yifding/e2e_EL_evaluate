import os
import argparse
from textwrap import wrap
from collections import defaultdict, deque

from nltk.tokenize import sent_tokenize

from e2e_EL_evaluate.utils.write_xml import write_annotation
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


'''
def count_set(doc_name2overlap_sent_index):
    print('doc_name2overlap_sent_index', doc_name2overlap_sent_index)
    return sum(len(value) for value in doc_name2overlap_sent_index.values())
'''

'''
def merge_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    ans = []
    for interval in intervals:
        if not ans or ans[-1][1] < interval[0]:
            ans.append(interval)
        else:
            ans[-1][1] = max(ans[-1][1], interval[1])
    return ans
'''


def doc_name_with_suffix(doc_name, start, end):
    return doc_name + '-' + str(start) + '_' + str(end)


'''
def merge_overlap_sent_index(doc_name2overlap_sent_index):
    ans = defaultdict(list)
    for doc_name in doc_name2overlap_sent_index:
        merge_out = merge_intervals(doc_name2overlap_sent_index[doc_name])
        ans[doc_name] = merge_out
    return ans
'''


def merged_sent(
            doc_name2txt,
            doc_name2start_end_txt,
            max_num_char=300,
            min_num_char=100,
        ):

    doc_name2merged_sent = dict()
    assert len(doc_name2txt) == len(doc_name2start_end_txt)

    for doc_name in doc_name2start_end_txt:
        start_end_txt = deque(doc_name2start_end_txt[doc_name])
        txt = doc_name2txt[doc_name]
        new_start_end_txt = []
        dq = deque([])
        cur_length = 0

        while start_end_txt:
            tmp_sent = start_end_txt.popleft()
            start, end = tmp_sent['start'], tmp_sent['end']
            dq.append(tmp_sent)

            cur_length += end - start

            if cur_length >= max_num_char:
                total_start = dq[0]['start']
                total_end = dq[-1]['end']
                new_start_end_txt.append(
                    {
                        'start': total_start,
                        'end': total_end,
                        'txt': txt[total_start: total_end]
                    }
                )

                cur_length = 0
                dq = deque([])

        if cur_length > 0:
            # **YD** consider minimum characters of the sentence
            if cur_length >= min_num_char:
                total_start = dq[0]['start']
                total_end = dq[-1]['end']
                new_start_end_txt.append(
                    {
                        'start': total_start,
                        'end': total_end,
                        'txt': txt[total_start: total_end]
                    }
                )

            elif len(new_start_end_txt) > 0:
                total_start = new_start_end_txt[-1]['start']
                total_end = dq[-1]['end']
                new_start_end_txt[-1]['end'] = total_end
                new_start_end_txt[-1]['txt'] = txt[total_start: total_end]

            # **YD** may cause some annotation missing with last sentence.
        doc_name2merged_sent[doc_name] = new_start_end_txt

    return doc_name2merged_sent


def obtain_pos(pos, start_end_txt, is_start=True):
    ans = -1
    for index, start_end in enumerate(start_end_txt):
        start = start_end['start']
        end = start_end['end']
        if is_start and start <= pos < end:
            ans = index
            return ans
        elif not is_start and start < pos <= end:
            ans = index
            return ans
    return ans


def obtain_pos_anno(anno, start_end_txt):
    start = anno['start']
    end = anno['end']
    ans_start = obtain_pos(start, start_end_txt, is_start=True)
    ans_end = obtain_pos(end, start_end_txt, is_start=False)

    if ans_start == -1 or ans_end == -1:
        print(anno, start_end_txt, ans_start, ans_end)
    # assert ans_start != -1
    # assert ans_end != -1

    return ans_start, ans_end


def revise_txt(doc_name2start_end_txt, doc_name2txt):
    doc_name2revised_txt = dict()
    for doc_name in doc_name2start_end_txt:
        start_end_txt = doc_name2start_end_txt[doc_name]
        txt = doc_name2txt[doc_name]
        for start_end in start_end_txt:
            start = start_end['start']
            end = start_end['end']
            doc_name_with_suffix_out = doc_name_with_suffix(doc_name, start, end)
            doc_name2revised_txt[doc_name_with_suffix_out] = txt[start: end]
    return doc_name2revised_txt


def check_anno_cross_sent_splits(doc_name2start_end_txt, doc_name2anno):
    doc_name2revised_anno = defaultdict(list)
    doc_name2removed_anno = dict()

    for doc_name in doc_name2anno:
        removed_anno_list = list()
        anno_list = doc_name2anno[doc_name]
        start_end_txt = doc_name2start_end_txt[doc_name]

        for index, anno in enumerate(anno_list):
            start_pos, end_pos = obtain_pos_anno(anno, start_end_txt)
            if start_pos == -1 or end_pos == -1:
                removed_anno_list.append(anno)

            elif start_pos != end_pos:
                assert start_pos < end_pos
                removed_anno_list.append(anno)
            else:
                suffix_start, suffix_end = start_end_txt[start_pos]['start'], start_end_txt[start_pos]['end']
                doc_name_with_suffix_out = doc_name_with_suffix(doc_name, suffix_start, suffix_end)
                new_anno = dict(anno)
                new_anno['start'] -= suffix_start
                new_anno['end'] -= suffix_start
                doc_name2revised_anno[doc_name_with_suffix_out].append(new_anno)

        doc_name2removed_anno[doc_name] = removed_anno_list

    return doc_name2revised_anno, doc_name2removed_anno


def sent_location(doc_name2txt, doc_name2txt_sent_splits):
    doc_name2start_end_txt = defaultdict(list)
    for doc_name in doc_name2txt:
        assert doc_name in doc_name2txt_sent_splits
        txt = doc_name2txt[doc_name]
        txt_sent_splits = doc_name2txt_sent_splits[doc_name]
        cur_index = 0

        for txt_sent_split in txt_sent_splits:
            pos = txt.find(txt_sent_split, cur_index)
            assert pos != -1

            start, end = pos, pos + len(txt_sent_split)
            cur_index = end
            doc_name2start_end_txt[doc_name].append(
                {
                    'start': start,
                    'end': end,
                    'txt': txt_sent_split,
                }
            )
    return doc_name2start_end_txt


def textwrap_sent_seg(txt_list, max_num_char):
    re_txt_list = []
    for txt in txt_list:
        if len(txt) > max_num_char:
            # see https://docs.python.org/3.7/library/textwrap.html#textwrap.TextWrapper
            split_txt = wrap(
                txt,
                width=max_num_char,
                expand_tabs=False,
                replace_whitespace=False,
                drop_whitespace=False,
                break_long_words=False,
                break_on_hyphens=False,
            )
            re_txt_list.extend(split_txt)
        else:
            re_txt_list.append(txt)
    return re_txt_list


def main(args):
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)

    for dataset in args.datasets:
        print('dataset', dataset)
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset, has_prob=args.has_prob)
        doc_name2txt_sent_splits = dict()

        for doc_name in doc_name2anno:
            tmp_anno = doc_name2anno[doc_name]
            tmp_anno = sorted(tmp_anno, key=lambda x: (x['start'], x['end']))
            doc_name2anno[doc_name] = tmp_anno

        # split sentences into multiple pieces
        for doc_name in doc_name2txt:
            # the result of sent_tokenize maybe too long, use "textwrap" of python to shorten them smaller than
            # the args.max_num_char.
            # doc_name2txt_sent_splits[doc_name] = sent_tokenize(doc_name2txt[doc_name])
            tmp_sent_list = sent_tokenize(doc_name2txt[doc_name])
            tmp_sent_list = textwrap_sent_seg(tmp_sent_list, args.max_num_char)
            doc_name2txt_sent_splits[doc_name] = tmp_sent_list

        doc_name2start_end_txt = sent_location(doc_name2txt, doc_name2txt_sent_splits)

        doc_name2merged_sent = merged_sent(
            doc_name2txt,
            doc_name2start_end_txt,
            max_num_char=args.max_num_char,
            min_num_char=args.min_num_char,
        )

        doc_name2revised_anno, doc_name2removed_anno = check_anno_cross_sent_splits(
            doc_name2merged_sent, doc_name2anno,
        )

        doc_name2revised_txt = revise_txt(doc_name2merged_sent, doc_name2txt)

        # 1. write split sentences and split annotations
        xml_file = os.path.join(args.output_dir, dataset + '/' + dataset + '.xml')
        remove_xml_file = os.path.join(args.output_dir, dataset + '/' + 'remove_' + dataset + '.xml')
        txt_dir = os.path.join(args.output_dir, dataset + '/RawText')
        os.makedirs(txt_dir, exist_ok=True)

        # **YD** sort the annotations by start first, and end second.
        for doc_name in doc_name2revised_anno:
            tmp = doc_name2revised_anno[doc_name]
            tmp = sorted(tmp, key=lambda x: (x['start'], x['end']))
            doc_name2revised_anno[doc_name] = list(tmp)

        # **YD** fix a bug missing the txt without annotation
        for doc_name in doc_name2revised_txt:
            txt_file = os.path.join(txt_dir, doc_name)
            with open(txt_file, 'w') as writer:
                writer.write(doc_name2revised_txt[doc_name])

        write_annotation(dataset, xml_file, doc_name2revised_anno, has_prob=args.has_prob)
        write_annotation(dataset, remove_xml_file, doc_name2removed_anno, has_prob=args.has_prob)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span',
        help='Specify the input xml annotation directory',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL/GT/aida',
        help='Specify the splits output xml directory',
    )

    parser.add_argument(
        "--datasets",
        default="['aida_testa', 'aida_testb', 'aida_train']",
        type=eval,
    )

    parser.add_argument(
        "--max_num_char",
        default=300,
        type=int,
    )

    parser.add_argument(
        "--min_num_char",
        default=100,
        type=int,
    )
    parser.add_argument(
        "--has_prob",
        action="store_true",
    )

    args = parser.parse_args()
    main(args)