import os
import argparse
from collections import defaultdict

from nltk.tokenize import sent_tokenize

from gen_anno_from_xml import gen_anno_from_xml


def count_set(doc_name2overlap_sent_index):
    print('doc_name2overlap_sent_index', doc_name2overlap_sent_index)
    return sum(len(value) for value in doc_name2overlap_sent_index.values())


def merge_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    ans = []
    for interval in intervals:
        if not ans or ans[-1][1] < interval[0]:
            ans.append(interval)
        else:
            ans[-1][1] = max(ans[-1][1], interval[1])
    return ans


def merge_overlap_sent_index(doc_name2overlap_sent_index):
    ans = defaultdict(list)
    for doc_name in doc_name2overlap_sent_index:
        merge_out = merge_intervals(doc_name2overlap_sent_index[doc_name])
        ans[doc_name] = merge_out
    return ans


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
        print(anno, start_end_txt)
    assert ans_start != -1
    assert ans_end != -1

    return ans_start, ans_end


def check_anno_cross_sent_splits(doc_name2start_end_txt, doc_name2anno):
    doc_name2overlap_sent_index = defaultdict(set)
    for doc_name in doc_name2anno:
        anno_list = doc_name2anno[doc_name]
        start_end_txt = doc_name2start_end_txt[doc_name]

        for index, anno in enumerate(anno_list):
            start_pos, end_pos = obtain_pos_anno(anno, start_end_txt)
            if start_pos != end_pos:
                assert start_pos < end_pos
                doc_name2overlap_sent_index[doc_name].add((start_pos, end_pos))

    return doc_name2overlap_sent_index


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


def main(args):
    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)

    for dataset in args.datasets:
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset)
        doc_name2txt_sent_splits = dict()
        for doc_name in doc_name2anno:
            tmp_anno = doc_name2anno[doc_name]
            tmp_anno = sorted(tmp_anno, key=lambda x: x['end'])
            tmp_anno = sorted(tmp_anno, key=lambda x: x['start'])
            doc_name2anno[doc_name] = tmp_anno

        # split sentences into multiple pieces
        for doc_name in doc_name2txt:
            doc_name2txt_sent_splits[doc_name] = sent_tokenize(doc_name2txt[doc_name])
        doc_name2start_end_txt = sent_location(doc_name2txt, doc_name2txt_sent_splits)
        doc_name2overlap_sent_index = check_anno_cross_sent_splits(doc_name2start_end_txt, doc_name2anno)
        num_set = count_set(doc_name2overlap_sent_index)
        print('dataset', dataset, 'num_set', num_set)

        doc_name2overlap_sent_index = merge_overlap_sent_index(doc_name2overlap_sent_index)
        print('merged_indices', doc_name2overlap_sent_index)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prediction/EL/GT/aida',
        help='Specify the input xml annotation directory',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/pre2split/EL/GT/aida',
        help='Specify the splits output xml directory',
    )

    parser.add_argument(
        "--datasets",
        default="['aida_testa', 'aida_testb', 'aida_train']",
        type=eval,
    )

    args = parser.parse_args()
    main(args)