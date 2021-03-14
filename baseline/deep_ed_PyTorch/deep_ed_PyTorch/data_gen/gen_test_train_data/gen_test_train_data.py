import os
import argparse

from deep_ed_PyTorch import utils
from deep_ed_PyTorch.data_gen.indexes import YagoCrosswikisWiki
from deep_ed_PyTorch.entities.ent_name2id_freq import EntNameID


class GenTestTrain(object):
    def __init__(self, args):
        self.args = args
        self.ctxt_len = 100
        self.num_cand = 100

        self.ent_name_id = EntNameID(args)
        self.yago_crosswikis_wiki = YagoCrosswikisWiki(args)

        # **YD** debug
        for dataset in args.datasets:
            self.gen_token_format(dataset)

        # self.gen_aida_train()
        # self.gen_aida_test()

    def gen_token_format(self, dataset='ace2004'):
        print('\nGenerating test data from dataset:' + dataset)

        if 'aida' in dataset:
            path = 'basic_data/test_datasets/Span_Format/AIDA/' + dataset
            path = os.path.join(self.args.root_data_dir, path)
        elif dataset in ['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia']:
            path = 'basic_data/test_datasets/Span_Format/wned/' + dataset
            path = os.path.join(self.args.root_data_dir, path)
        else:
            raise ValueError('Unknown Dataset: {}!'.format(dataset))

        out_dir = os.path.join(self.args.root_data_dir, 'generated/test_train_data')
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, dataset + '.csv')
        anno_file = os.path.join(path, dataset + '.xml')

        print('input main path: ', path)
        assert os.path.isdir(path)
        print('anno_file: ', anno_file)
        assert os.path.isfile(anno_file)
        print('out_file: ', out_file)
        # assert os.path.isfile(out_file)

        writer = open(out_file, 'w')
        reader = open(anno_file, 'r')

        num_NER = 0
        num_EL = 0
        num_nonexistent_ent_id = 0
        num_correct_ents = 0

        cur_doc_text = ''
        cur_doc_name = ''

        line = reader.readline()
        while line:
            doc_str_start = 'document docName=\"'
            doc_str_end = '\">'

            if doc_str_start in line:
                start = line.find(doc_str_start)
                end = line.find(doc_str_end)
                cur_doc_name = line[start + len(doc_str_start): end]
                cur_doc_name = cur_doc_name.replace('&amp;', '&')
                cur_doc_text = ''
                assert os.path.isfile(os.path.join(path, 'RawText/' + cur_doc_name))
                with open(os.path.join(path, 'RawText/' + cur_doc_name), 'r') as raw_reader:
                    for txt_line in raw_reader:
                        cur_doc_text += txt_line
                cur_doc_text = cur_doc_text.replace('&amp;', '&')

            else:
                if '<annotation>' in line:

                    line = reader.readline()
                    assert '<mention>' in line and '</mention>' in line
                    m_start = line.find('<mention>') + len('<mention>')
                    m_end = line.find('</mention>')
                    cur_mention = line[m_start: m_end]
                    cur_mention = cur_mention.replace('&amp;', '&')

                    line = reader.readline()
                    # assert '<wikiName>' in line and '</wikiName>' in line
                    e_start = line.find('<wikiName>') + len('<wikiName>')
                    e_end = line.find('</wikiName>')
                    cur_ent_title = '' if '<wikiName/>' in line else line[e_start: e_end]
                    cur_ent_title = cur_ent_title.replace('&amp;', '&')

                    line = reader.readline()
                    assert '<offset>' in line and '</offset>' in line
                    off_start = line.find('<offset>') + len('<offset>')
                    off_end = line.find('</offset>')
                    offset = int(line[off_start: off_end])

                    line = reader.readline()
                    assert '<length>' in line and '</length>' in line
                    len_start = line.find('<length>') + len('<length>')
                    len_end = line.find('</length>')
                    length = int(line[len_start: len_end])
                    assert length == len(cur_mention)
                    #length = len(cur_mention)

                    line = reader.readline()
                    if '<entity/>' in line:
                        line = reader.readline()

                    assert '</annotation>' in line

                    # strictly require the annotation mention equals to the span mention.
                    assert cur_doc_text[offset: offset + length] == cur_mention

                    # **YD** preprocess_mention has been implemented
                    cur_mention = self.yago_crosswikis_wiki.preprocess_mention(cur_mention)

                    if cur_ent_title == 'NIL' or cur_ent_title == '':
                        num_NER += 1
                    else:
                        num_EL += 1
                        # **YD** get_ent_wikiid_from_name has been implemented
                        cur_ent_wikiid = self.ent_name_id.get_ent_wikiid_from_name(cur_ent_title)

                        # **YD** unk_ent_wikiid has been implemented
                        if cur_ent_wikiid == self.ent_name_id.unk_ent_wikiid:
                            num_nonexistent_ent_id += 1
                            print('unknown entity anno: ', cur_ent_title)
                        else:
                            num_correct_ents += 1

                        assert len(cur_mention) > 0

                        # s = cur_doc_name + '\t' + cur_doc_name + '\t' + cur_mention + '\t'
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

                        writer.write(s)

            line = reader.readline()

        writer.close()

        print('Done '+ dataset + '.')
        print('num_NER', num_NER, 'num_EL', num_EL)
        print('num_nonexistent_ent_id = ' + str(num_nonexistent_ent_id) + '; num_correct_ents = ' + str(num_correct_ents))


def test(args):
    GenTestTrain(args)


def eval_str_list(x, type=float):
    if x is None:
        return None
    if isinstance(x, str):
        x = eval(x)
    try:
        return list(map(type, x))
    except TypeError:
        return [type(x)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='evaluate the coverage percent of entity dictionary on evaluate GT entity'
    )

    parser.add_argument(
        '--root_data_dir',
        type=str,
        default='/scratch365/yding4/EL_resource/data/deep_ed_PyTorch_data/',
        help='Root path of the data, $DATA_PATH.',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        default="['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_train', 'aida_testa', 'aida_testb']",
        help='Root path of the data, $DATA_PATH.',
    )

    args = parser.parse_args()
    print(args)
    test(args)