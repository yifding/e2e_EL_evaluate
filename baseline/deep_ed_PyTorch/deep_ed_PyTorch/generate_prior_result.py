# evaluate entity linking from prior dictionary of "joint learning" EMNLP 2017
# parts = line.strip('\r\n').split('\t')
# parts[0] = ID of article
# parts[1] = start_end
# parts[2] = mention
# parts[3] = left_context
# parts[4] = right_context
# parts[5] = 'CANDIDATES'
# parts[6:-2]: candidates
# parts[-2]: GT:
# parts[-1]: -1 or '-1,' + str(cur_ent_wikiid) + ',' + cur_ent_title or str(gt_pos) + ',' + candidates[gt_pos] or '-1,' + str(cur_ent_wikiid) + ',' + cur_ent_title


"""
# https://github.com/yifding/e2e_EL_evaluate/blob/main/baseline/deep_ed_PyTorch/
# deep_ed_PyTorch/data_gen/gen_test_train_data/gen_test_train_data.py
s = cur_doc_name + '\t' + str(offset) + '_' + str(length) + '\t' + cur_mention + '\t'
# **YD** split_in_words has been implemented, should return a list
left_words = utils.split_in_words(cur_doc_text[0: offset])
left_ctxt = left_words[-self.ctxt_len:]
if len(left_ctxt) == 0:
    left_ctxt.append('EMPTYCTXT')
s += ' '.join(left_ctxt) + '\t'

# **YD** split_in_words not implemented, should return a list
right_words = utils.split_in_words(cur_doc_text[offset + length:])
right_ctxt = right_words[:self.ctxt_len]
if len(right_ctxt) == 0:
    right_ctxt.append('EMPTYCTXT')
s += ' '.join(right_ctxt) + '\tCANDIDATES\t'


# Entity candidates from p(e|m) dictionary
# **YD** ent_p_e_m_index has been implemented
if cur_mention in self.yago_crosswikis_wiki.ent_p_e_m_index and \
        len(self.yago_crosswikis_wiki.ent_p_e_m_index[cur_mention]) > 0:
    sorted_cand = sorted(self.yago_crosswikis_wiki.ent_p_e_m_index[cur_mention].items(),
                         key=lambda x: x[1], reverse=True)

    candidates = []
    gt_pos = -1

    for index, (wikiid, p) in enumerate(sorted_cand[: self.num_cand]):
        # **YD** get_ent_wikiid_from_name has been implemented
        candidates.append(str(wikiid) + ',' + '{0:.3f}'.format(p) + ',' + \
                          self.ent_name_id.get_ent_name_from_wikiid(wikiid))

        if wikiid == cur_ent_wikiid:
            # **YD** index is based on python array, start with 0
            gt_pos = index

    s += '\t'.join(candidates) + '\tGT:\t'

    if gt_pos >=0:
        s += str(gt_pos) + ',' + candidates[gt_pos] + '\n'
    else:
        # **YD** unk_ent_wikiid has been implemented
        if cur_ent_wikiid != self.ent_name_id.unk_ent_wikiid:
            s += '-1,' + str(cur_ent_wikiid) + ',' + cur_ent_title + '\n'

        else:
            s += '-1\n'

else:
    # **YD** unk_ent_wikiid has been not implemented
    if cur_ent_wikiid != self.ent_name_id.unk_ent_wikiid:
        s += 'EMPTYCAND\tGT:\t-1,' + str(cur_ent_wikiid) + ',' + cur_ent_title + '\n'
    else:
        s += 'EMPTYCAND\tGT:\t-1\n'

"""


import os
import argparse
from collections import defaultdict


def main(args):
    for dataset in args.datasets:
        print(dataset)

        file = os.path.join(args.input_dir, dataset + '.csv')

        os.makedirs(args.output_dir, exist_ok=True)
        output = os.path.join(args.output_dir, dataset + '.csv')
        writer = open(output, 'w')

        with open(file, 'r') as reader:
            for i, line in enumerate(reader):
                parts = line.rstrip('\n').split('\t')
                doc_name = parts[0]
                start_end = parts[1]
                mention = parts[2]
                left_context, right_context = parts[3], parts[4]

                assert parts[5] == 'CANDIDATES'
                assert parts[-2] == 'GT:'
                candidates = parts[6:-2]

                last_part = parts[-1]
                last_splits = last_part.split(',')

                s = doc_name + '\t' + start_end + '\t' + mention + '\t'
                if candidates[0] != 'EMPTYCAND':
                    # cand_splits = candidates[0].split(',')
                    # wikiid, p, ent_name = cand_splits[0], cand_splits[1], cand_splits[2]
                    s += candidates[0] + '\t'
                else:
                    s += 'EMPTYCAND' + '\t'

                s += '\n'
                writer.write(s)

        writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='process aida data to xml format'
    )

    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data/generated/test_train_data',
        help='Specify the input directory',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data/visualization/prior/',
        help='Specify the output directory',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        default="['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_train', 'aida_testa', 'aida_testb']",
        help='datasets',
    )

    args = parser.parse_args()
    main(args)
