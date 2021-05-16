import os
import argparse
from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES, XMLModel2DBModel
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.evaluation.confusion_matrix_from_xml import confusion_matrix_from_xml, compute_metric

def main(args):
    # 1. obtain the union of annotations.
    stats_list = []
    for dataset in args.datasets:
        assert dataset in DATASET2DATASET_TYPES
        dataset_type = DATASET2DATASET_TYPES[dataset]
        union_doc_name2txt = dict()
        union_doc_name2anno = dict()
        for xml_model in XMLModel2DBModel:
            input_dir = os.path.join(args.input_verify_dir, xml_model + '/' + dataset_type)
            doc_name2txt, doc_name2anno = gen_anno_from_xml(input_dir, dataset)
            for doc_name in doc_name2txt:
                if doc_name not in union_doc_name2txt:
                    union_doc_name2txt[doc_name] = doc_name2txt[doc_name]
                else:
                    assert union_doc_name2txt[doc_name] == doc_name2txt[doc_name]

            for doc_name in doc_name2anno:
                if doc_name not in union_doc_name2anno:
                    union_doc_name2anno[doc_name] = []
                for anno in doc_name2anno[doc_name]:
                    if anno not in union_doc_name2anno[doc_name]:
                        union_doc_name2anno[doc_name].append(anno)

        # 2. obtain the model annotations.
        for xml_model in args.models:
            print('model', xml_model)
            model_xml_dir = os.path.join(args.model_xml_dir, xml_model + '/' + dataset_type)
            model_doc_name2txt, model_doc_name2anno = gen_anno_from_xml(model_xml_dir, dataset)

            # 3. update the num_anno computation in GT.
            stats = confusion_matrix_from_xml(
                union_doc_name2txt,
                model_doc_name2anno,
                union_doc_name2anno,
                is_strong_match=args.is_strong_match,
                method=args.method,
            )

            stats_list.append(stats)

    total_stats = dict()
    for key in stats_list[0].keys():
        total_stats[key] = 0

    for stats in stats_list:
        for key, value in stats.items():
            total_stats[key] += value

    metric = compute_metric(total_stats)
    print(metric)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='compute micro/macro precision/recall/f1 from xml directory and dataset',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--model_xml_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_subset_xml_EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--input_verify_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_xml_EL',
        help='Specify the splits output directory for the db download file',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        default="['ace2004','aquaint','clueweb','msnbc','wikipedia','aida_testa','aida_testb','aida_train']",
        help='datasets for EL',
    )

    parser.add_argument(
        '--models',
        type=eval,
        default="['GT','rel','end2end_neural_el']",
        help='XMLModel models for EL',
    )

    parser.add_argument(
        '--method',
        type=str,
        default='greedy',
        choices=['', 'ILP', 'greedy'],
        help='compute number of computed GT annotations',
    )

    parser.add_argument(
        '--is_strong_match',
        action="store_true",
        help='strong match or not (weak match)',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.input_verify_dir)
    main(args)