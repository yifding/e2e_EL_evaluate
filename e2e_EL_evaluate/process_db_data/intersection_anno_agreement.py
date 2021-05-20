import os
import argparse
from collections import defaultdict

from e2e_EL_evaluate.utils.constants import DATASET2DATASET_TYPES, XMLModel2DBModel
from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml
from e2e_EL_evaluate.utils.collect_dataset2doc_name import collect_dataset2doc_name

# (1). (Done in the previous processing steps)find shared doc_names in the datasets for verification across models.
# (2). find shared annotation across models within the doc_names in (1).
# (3). for each anno in (2), stats its agreement # of (verify, edit, remove) across different models.


def main(args):
    dataset2model2doc_name2anno = dict()
    dataset2doc_name2shared_anno = dict()
    start_model = list(XMLModel2DBModel.keys())[0]

    for dataset in DATASET2DATASET_TYPES:
        dataset_type = DATASET2DATASET_TYPES[dataset]

        assert dataset not in dataset2model2doc_name2anno
        dataset2model2doc_name2anno[dataset] = dict()
        assert dataset not in dataset2doc_name2shared_anno
        dataset2doc_name2shared_anno[dataset] = dict()

        for model in XMLModel2DBModel:
            assert model not in dataset2model2doc_name2anno[dataset]
            subset_ori_xml_path = os.path.join(args.subset_ori_xml_output_dir, model + '/' + dataset_type)
            doc_name2txt, doc_name2anno = gen_anno_from_xml(subset_ori_xml_path, dataset)
            dataset2model2doc_name2anno[dataset][model] = doc_name2anno

        # start_model = list(XMLModel2DBModel.keys())[0]
        for doc_name in dataset2model2doc_name2anno[dataset][start_model]:
            for anno in dataset2model2doc_name2anno[dataset][start_model][doc_name]:
                is_intersect = True
                for follow_model in list(XMLModel2DBModel.keys())[1:]:
                    if doc_name not in dataset2model2doc_name2anno[dataset][follow_model] or \
                       anno not in dataset2model2doc_name2anno[dataset][follow_model][doc_name]:
                        is_intersect = False
                        break

                if is_intersect:
                    if doc_name not in dataset2doc_name2shared_anno[dataset]:
                        dataset2doc_name2shared_anno[dataset][doc_name] = []
                    dataset2doc_name2shared_anno[dataset][doc_name].append(anno)

    dataset2model2doc_name2verify_anno = dict()
    for dataset in DATASET2DATASET_TYPES:
        dataset_type = DATASET2DATASET_TYPES[dataset]
        assert dataset not in dataset2model2doc_name2verify_anno
        dataset2model2doc_name2verify_anno[dataset] = dict()
        for model in XMLModel2DBModel:
            assert model not in dataset2model2doc_name2verify_anno[dataset]

            intersect_xml_path = os.path.join(args.intersect_xml_output_dir, model + '/' + dataset_type)
            doc_name2txt, doc_name2anno = gen_anno_from_xml(intersect_xml_path, dataset)
            dataset2model2doc_name2verify_anno[dataset][model] = doc_name2anno

    # dataset2doc_name2shared_anno
    # dataset2model2doc_name2verify_anno
    dataset2counter = dict()
    dataset2coarse_counter = dict()
    for dataset in dataset2doc_name2shared_anno:
        dataset2counter[dataset] = defaultdict(int)
        dataset2coarse_counter[dataset] = defaultdict(int)
        model2doc_name2verify_anno = dataset2model2doc_name2verify_anno[dataset]
        for doc_name in dataset2doc_name2shared_anno[dataset]:
            for shared_anno in dataset2doc_name2shared_anno[dataset][doc_name]:
                start, end, mention_txt, entity_txt = \
                    shared_anno['start'], shared_anno['end'], shared_anno['mention_txt'], shared_anno['entity_txt']

                verify = 0
                edit = 0
                remove = 0
                for model in XMLModel2DBModel:
                    doc_name2verify_anno = model2doc_name2verify_anno[model]
                    assert doc_name in doc_name2verify_anno
                    find_flag = False
                    for verify_anno in doc_name2verify_anno[doc_name]:
                        if verify_anno['start'] == start and verify_anno['end'] == end:
                            find_flag = True
                            if verify_anno['entity_txt'] == entity_txt:
                                verify += 1
                            else:
                                edit += 1
                            break
                    if not find_flag:
                        remove += 1
                dataset2counter[dataset][(verify, edit, remove)] += 1
                dataset2coarse_counter[dataset][verify] += 1
    #print(dataset2counter)
    print(dataset2coarse_counter)


def parse_args():
    parser = argparse.ArgumentParser(
        description='process aida data to xml format',
        allow_abbrev=False,
    )

    parser.add_argument(
        '--intersect_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_xml_EL',
        help='Specify the intersection output directory for the output xml',
    )

    parser.add_argument(
        '--subset_ori_xml_output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_subset_xml_EL',
        help='Specify the intersection output directory for the output xml',
    )

    args = parser.parse_args()
    assert os.path.isdir(args.intersect_xml_output_dir)
    assert os.path.isdir(args.subset_ori_xml_output_dir)

    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)
