import os
import argparse
from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.extract_subset_xml import extract_subset_xml


# The annotation format is a dictionary of list
# the key of the dictionary is the doc_name while each element of the list is a dictionary

# anno = {
#   'testa_1001': [
#       {
#       'start': ,
#       'end',
#       'mention_txt': ,
#       'entity_txt': ,
#        }
#   ]
# }


class ConfusionMatrix(object):
    def __init__(self, TP, TN, FP, FN):
        self.TP = TP
        self.TN = TN
        self.FP = FP
        self.FN = FN

    @property
    def recall(self):
        return self.TP / (self.TP + self.FN)

    @property
    def precision(self):
        return self.TP / (self.TP + self.FP)

    @property
    def F1(self):
        if not self.recall == 0 and self.precision == 0:
            return 2 * self.recall * self.precision / (self.recall + self.precision)
        else:
            print('recall and precision are both 0!')
            return 0


def strong_match_TP(txt, model_anno_list, GT_anno_list):
    """
    :param txt: a string to represent the a document.
    :param model_anno_list: annotation list from a model.
    :param GT_anno_list: annotation list from a "Ground Truth".
    :return: number of true positive samples.

    the reason includes the txt is to make sure the mentions are present and correct.
    """
    TP = 0
    for anno in model_anno_list + GT_anno_list:
        start, end, mention = anno['start'], anno['end'], anno['mention_txt']
        assert txt[start: end] == mention

    for model_anno in model_anno_list:
        model_start, model_end, model_mention, model_entity = \
            model_anno['start'], model_anno['end'], model_anno['mention_txt'], model_anno['entity_txt']
        for GT_anno in GT_anno_list:
            GT_start, GT_end, GT_mention, GT_entity = \
                GT_anno['start'], GT_anno['end'], GT_anno['mention_txt'], GT_anno['entity_txt']

            if model_start == GT_start and model_end == GT_end and \
                    model_mention == GT_mention and model_entity == GT_entity:
                TP += 1
                break

    return TP


def weak_match_TP(txt, model_anno_list, GT_anno_list):
    """
    :param txt: a string to represent the a document.
    :param model_anno_list: annotation list from a model.
    :param GT_anno_list: annotation list from a "Ground Truth".
    :return: number of true positive samples.

    the reason includes the txt is to make sure the mentions are present and correct.
    """
    TP = 0
    for anno in model_anno_list + GT_anno_list:
        start, end, mention = anno['start'], anno['end'], anno['mention_txt']
        assert txt[start: end] == mention

    for model_anno in model_anno_list:
        model_start, model_end, model_mention, model_entity = \
            model_anno['start'], model_anno['end'], model_anno['mention_txt'], model_anno['entity_txt']
        for GT_anno in GT_anno_list:
            GT_start, GT_end, GT_mention, GT_entity = \
                GT_anno['start'], GT_anno['end'], GT_anno['mention_txt'], GT_anno['entity_txt']

            if model_entity == GT_entity and \
                    (
                        GT_start <= model_start < GT_end or
                        model_start <= GT_start < model_end
                    ):
                TP += 1
                break

    return TP


def num_anno(anno, method=''):
    if method == '':
        return len(anno)
    else:
        raise ValueError('Unsupported method!')


def confusion_matrix_from_xml(
        doc_name2txt,
        model_doc_name2anno,
        GT_doc_name2anno,
        is_strong_match=True,
):
    for doc_name in model_doc_name2anno:
        assert doc_name in doc_name2txt

    for doc_name in GT_doc_name2anno:
        assert doc_name in doc_name2txt

    TP = 0
    acum_precision = 0
    acum_recall = 0
    num_doc_model = 0
    num_doc_GT = 0

    for doc_name in doc_name2txt:
        txt = doc_name2txt[doc_name]
        model_anno_list = model_doc_name2anno[doc_name] if doc_name in model_doc_name2anno else []
        GT_anno_list = GT_doc_name2anno[doc_name] if doc_name in GT_doc_name2anno else []
        if is_strong_match:
            tmp_TP = strong_match_TP(txt, model_anno_list, GT_anno_list)
        else:
            tmp_TP = weak_match_TP(txt, model_anno_list, GT_anno_list)

        if tmp_TP > 0:
            num_doc_model += 1
            acum_precision += tmp_TP / num_anno(model_anno_list)

        if num_anno(GT_anno_list) > 0:
            num_doc_GT += 1
            acum_recall += tmp_TP / num_anno(GT_anno_list)

        TP += tmp_TP

    micro_precision = TP / sum(num_anno(value) for value in model_doc_name2anno.values())
    micro_recall = TP / sum(num_anno(value) for value in GT_doc_name2anno.values())

    if micro_precision * micro_recall > 0:
        micro_F1 = 2 * micro_precision * micro_recall / (micro_precision + micro_recall)
    else:
        micro_F1 = None

    if num_doc_model > 0:
        macro_precision = acum_precision / num_doc_model
    else:
        macro_precision = None

    if num_doc_GT > 0:
        macro_recall = acum_recall / num_doc_GT
    else:
        macro_recall = None

    if macro_precision is not None and macro_recall is not None and macro_precision != 0 and macro_recall != 0:
        macro_F1 = 2 * macro_precision * macro_recall / (macro_precision + macro_recall)
    else:
        macro_F1 = None

    print('is_strong_match:', is_strong_match)
    print('total documentation:', len(doc_name2txt), ' num_doc_model:', num_doc_model, ' num_doc_GT:', num_doc_GT)
    print('micro_precision', micro_precision, 'micro_recall', micro_recall, 'micro_F1', micro_F1)
    print('macro_precision', macro_precision, 'macro_recall', macro_recall, 'macro_F1', macro_F1)

    return {
        'micro_precision': micro_precision,
        'micro_recall': micro_recall,
        'micro_F1': micro_F1,
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'macro_F1': macro_F1,
    }


def main(args):
    print("compute micro/macro precision/recall/f1 from xml directory and dataset...")
    print("model", args.model_model, "dataset", args.dataset)
    model_xml_path = os.path.join(args.model_xml_dir, args.model_model + '/' + DATASET2DATASET_TYPES[args.dataset])
    # model_doc_name2txt, model_doc_name2anno = gen_anno_from_xml(model_xml_path, args.dataset)

    GT_xml_path = os.path.join(args.GT_xml_dir, args.GT_model + '/' + DATASET2DATASET_TYPES[args.dataset])
    # GT_doc_name2txt, GT_doc_name2anno = gen_anno_from_xml(GT_xml_path, args.dataset)

    subset_doc_name2txt, subset_doc_name2anno, full_new_doc_name2anno = extract_subset_xml(
        subset_xml_dir=model_xml_path,
        subset_dataset=args.dataset,
        full_xml_dir=GT_xml_path,
        full_dataset=args.dataset,
    )

    confusion_matrix_from_xml(
        subset_doc_name2txt,
        subset_doc_name2anno,
        full_new_doc_name2anno,
        is_strong_match=args.is_strong_match,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='compute micro/macro precision/recall/f1 from xml directory and dataset',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--model_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/intersect_xml_EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--GT_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/intersect_xml_EL',
        help='Specify the splits output directory for the output xml directory from DB process results',
    )

    parser.add_argument(
        '--model_model',
        type=str,
        default='end2end_neural_el',
        choices=['GT','rel','end2end_neural_el'],
        help='models for EL',
    )

    parser.add_argument(
        '--GT_model',
        type=str,
        default='GT',
        choices=['GT', 'rel', 'end2end_neural_el'],
        help='models for EL',
    )

    parser.add_argument(
        '--dataset',
        type=str,
        default='aida_testa',
        choices=['ace2004','aquaint','clueweb','msnbc','wikipedia','aida_testa','aida_testb','aida_train'],
        help='datasets for EL',
    )

    parser.add_argument(
        '--is_strong_match',
        action="store_true",
        help='strong match or not (weak match)',
    )

    args = parser.parse_args()
    main(args)