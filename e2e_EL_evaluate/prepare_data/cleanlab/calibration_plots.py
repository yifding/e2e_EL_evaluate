import os
import json
import argparse

import numpy as np


def main(args):
    # input_dir = "/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input/end2end_neural"
    # output_dir = "/scratch365/yding4/e2e_EL_evaluate/data/has_prob/calibration_plots/end2end_neural"
    # output_file = "end2end_neural.csv"
    # datasets = "['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']"
    # datasets = eval(datasets)
    input_dir = args.input_dir
    output_dir = args.output_dir
    output_file = os.path.join(args.output_dir, args.output_file)
    datasets = args.datasets
    num_bin = args.num_bin

    s = ""
    for dataset in datasets:
        input_file = os.path.join(input_dir, dataset + '.json')
        # output_file = os.path.join(output_dir, dataset + '.json')

        with open(input_file) as reader:
            dic = json.load(reader)

        sorted_dic = sorted(dic.items(), key=lambda x: x[1]["prob"])
        num_correct = sum(1 for ele in sorted_dic if ele[1]["correctness"])

        # print(sorted_dic[:5])
        # break
        # 1. compute the total number of positive samples

        splits = np.array_split(sorted_dic, num_bin)
        # print("type(splits)", type(splits))

        avg_prob_list = []
        accum_pos_fraction_list = []
        cur_frac = 0.0

        for index, split in enumerate(splits):
            avg_prob = sum(ins[1]["prob"] for ins in split) / len(split)
            cur_frac += sum(1 for ins in split if ins[1]["correctness"]) / num_correct
            avg_prob_list.append(avg_prob)
            accum_pos_fraction_list.append(cur_frac)

        avg_prob_list = [str(avg_prob) for avg_prob in avg_prob_list]
        accum_pos_fraction_list = [str(accum_pos_fraction) for accum_pos_fraction in accum_pos_fraction_list]

        # print(f"dataset: {dataset}, avg_prob_list: {avg_prob_list}, accum_pos_fraction_list: {accum_pos_fraction_list}")

        s += dataset + ',' + "avg_prob_list" + ',' + ','.join(avg_prob_list) + '\n'
        s += dataset + ',' + "accum_pos_fraction_list" + ',' + ','.join(accum_pos_fraction_list) + '\n'

    with open(output_file, 'w') as writer:
        writer.write(s)


def parse_args():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        "--input_dir",
        required=True,
        # default="/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input/end2end_neural",
        type=str,
    )
    parser.add_argument(
        "--output_dir",
        required=True,
        # default="/scratch365/yding4/e2e_EL_evaluate/data/has_prob/calibration_plots/end2end_neural",
        type=str,
    )
    parser.add_argument(
        "--output_file",
        required=True,
        # default="end2end_neural.csv",
        type=str,
    )
    parser.add_argument(
        "--datasets",
        required=True,
        # default="['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']",
        type=eval,
    )
    parser.add_argument(
        "--num_bin",
        default=10,
        type=int,
    )
    args = parser.parse_args()

    assert os.path.isdir(args.input_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    return args


if __name__ == "__main__":
    args = parse_args()

    main(args)