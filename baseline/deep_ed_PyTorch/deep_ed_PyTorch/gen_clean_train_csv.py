import os
import argparse

# because using the current pipeline to generate training csv file in 'generated/test_train_data/aida_train'
# generate corresponding clean file (GT entity in the top num_cand entities)


def arg_parse():

    parser = argparse.ArgumentParser(
            description='parser for ed model',
            allow_abbrev=False,
        )

    parser.add_argument(
        '--root_data_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data/',
        help='Root path of the data, $DATA_PATH.',
    )

    parser.add_argument(
        '--train_file',
        type=str,
        default='aida_train.csv',
        help='training csv file',
    )

    parser.add_argument(
        '--out_file',
        type=str,
        default='aida_train_clean.csv',
        help='training csv file',
    )

    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    input_file = os.path.join(args.root_data_dir, 'generated/test_train_data/' + args.train_file)
    output_file = os.path.join(args.root_data_dir, 'generated/test_train_data/' + args.out_file)

    num_line = 0
    num_valid_line = 0
    writer = open(output_file, 'w')
    len_set = set()
    with open(input_file, 'r') as reader:
        for line in reader:
            num_line += 1
            clean_line = line.rstrip('\n')
            last_part = clean_line.split('\t')[-1]
            last_part_split = last_part.split(',')
            len_set.add(len(last_part_split))
            if len(last_part_split) >= 4 and int(last_part_split[0]) >= 0:
                writer.write(line)
                num_valid_line += 1

    writer.close()
    print('len_set', len_set)
    print('num_valid_line', num_valid_line, 'num_line', num_line)


if __name__ == '__main__':
    main()


