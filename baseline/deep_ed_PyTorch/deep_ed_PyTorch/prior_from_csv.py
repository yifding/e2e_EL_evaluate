# evaluate entity linking from prior dictionary of "joint learning" EMNLP 2017
# parts = line.strip('\r\n').split('\t')
# parts[0] = ID of article
# parts[1] = parts[0]
# parts[2] = mention
# parts[3] =

import os
import argparse
from collections import defaultdict


def EvaluateRank(rank_list, empty_cand):
    """
    :param rank_list: a list of rank, -1 means not found, other means index starting from 0
    :return: coverage, avg_rank, avg_reverse_rank
    """

    avg_rank = 0
    avg_reverse_rank = 0
    uncoverage = 0
    tp = 0
    for i in rank_list:
        if 0 in rank_list:
            if i != -1:
                i = i + 1
        if i == -1:
            uncoverage += 1
        else:
            avg_rank += i
            avg_reverse_rank += 1 / i
            if i == 1:
                tp += 1

    avg_rank /= len(rank_list)
    avg_reverse_rank /= len(rank_list)
    uncoverage /= len(rank_list)
    coverage = 1 - uncoverage

    precision = tp / (len(rank_list) - empty_cand)
    recall = tp / len(rank_list)
    micro_f1 = 2 * precision * recall / (precision + recall)

    print('tp', tp)
    print('total_len', len(rank_list))
    print('total_non_empty_cand', len(rank_list) - empty_cand)
    print('precision', precision)
    print('recall', recall)
    print('micro_f1', micro_f1)
    print('coverage', coverage)
    print('avg_rank', avg_rank)
    print('avg_reverse_rank', avg_reverse_rank)


def main(args):
    directory = args.input_dir
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('csv')]
    #files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('csv') and 'aida' in f]


    rank_list_dict = defaultdict(list)

    empty_cand = 0
    for file in files:
        #if 'ace2004' not in file:
        #    continue

        empty_cand = 0
        with open(file, 'r') as reader:
            name = file.split('/')[-1][:-4]
            print(name)
            for i, line in enumerate(reader):
                parts = line.strip('\r\n').split('\t')
                # assert parts[0] == parts[1]
                rank = int(parts[-1].split(',')[0])
                if rank == -1:
                    if parts[-3] == 'EMPTYCAND':
                        empty_cand += 1
                rank_list_dict[name].append(rank)
            print("length:", i+1, 'empty', empty_cand)
            rank_list = rank_list_dict[name]
            EvaluateRank(rank_list, empty_cand)
            print('\n\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/EL_resource/baseline/deep_ed/deep-ed_data/generated/test_train_data',
        help='Specify the input AIDA directory',
    )

    args = parser.parse_args()
    main(args)

