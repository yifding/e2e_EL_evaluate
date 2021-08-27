import os
import json
import argparse
import collections

from e2e_EL_evaluate.evaluation.confusion_matrix_from_xml import (
    confusion_matrix_from_xml,
    compute_metric,
)
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES, XMLModel2DBModel
from e2e_EL_evaluate.utils.extract_subset_xml import extract_subset_xml

def main(args):
    for dataset in DATASET2DATASET_TYPES:
        dataset_type = DATASET2DATASET_TYPES[dataset]
        model_xml_path = os.path.join(args.model_xml_dir, args.model_model + '/' + dataset_type)
        GT_xml_path = os.path.join(args.GT_xml_dir, args.GT_model + '/' + dataset_type)


        # model_doc_name2txt, model_doc_name2anno = gen_anno_from_xml(model_xml_path, dataset)
        # GT_doc_name2txt, GT_doc_name2anno = gen_anno_from_xml(GT_xml_path, dataset)

        subset_doc_name2txt, subset_doc_name2anno, full_new_doc_name2anno = extract_subset_xml(
            subset_xml_dir=GT_xml_path,
            subset_dataset=dataset,
            full_xml_dir=model_xml_path,
            full_dataset=dataset,
        )
        GT_doc_name2anno = subset_doc_name2anno
        model_doc_name2anno = full_new_doc_name2anno


        model_entity2gt_entity2count = dict()
        for doc_name in model_doc_name2anno:
            model_annos = model_doc_name2anno[doc_name]
            if doc_name in GT_doc_name2anno:
                gt_annos = GT_doc_name2anno[doc_name]
            else:
                gt_annos = []
            for model_anno in model_annos:
                model_start = model_anno['start']
                model_end = model_anno['end']
                model_entity = model_anno['entity_txt']

                gt_entity = 'NIL'
                for tmp_gt_anno in gt_annos:
                    if tmp_gt_anno['start'] == model_start and tmp_gt_anno['end'] == model_end:
                        gt_entity = tmp_gt_anno['entity_txt']
                        break

                if model_entity not in model_entity2gt_entity2count:
                    model_entity2gt_entity2count[model_entity] = collections.defaultdict(int)
                model_entity2gt_entity2count[model_entity][gt_entity] += 1

        json_file = dataset + '.json'
        with open(args.GT_model + '_' + json_file, 'w') as writer:
            writer.write(json.dumps(model_entity2gt_entity2count, indent=4))

        '''
        stats = confusion_matrix_from_xml(
            model_doc_name2txt,
            model_doc_name2anno,
            GT_doc_name2anno,
            is_strong_match=False,
        )

        metrics = compute_metric(stats)
        print('dataset: ', dataset)
        print(metrics)
        '''


def parse_args():
    parser = argparse.ArgumentParser(
        description='list the six categories of annotation between GT and union of verified annotations',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--model_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/collect_pkl_rewrite_xml_EL',
        help='Specify the splits input directory for the db download file',
    )

    parser.add_argument(
        '--GT_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/label_xml_EL',
        help='Specify the splits input directory for the db download file',
    )

    parser.add_argument(
        '--model_model',
        type=str,
        default='GT',
        choices=['rel','GT','end2end_neural_el'],
        help='Specify the model of model',
    )

    parser.add_argument(
        '--GT_model',
        type=str,
        default='GT',
        choices=['rel', 'GT', 'end2end_neural_el'],
        help='Specify the model of GT',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.model_xml_dir)
    assert os.path.isdir(args.GT_xml_dir)

    # make sure the models are the same for model prediction and ground truth
    assert args.model_model == args.GT_model

    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)