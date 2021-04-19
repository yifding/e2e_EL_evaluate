import os
import argparse

from e2e_EL_evaluate.utils.gen_anno_from_xml import gen_anno_from_xml


def extract_subset_xml(subset_xml_dir, subset_dataset, full_xml_dir, full_dataset):
    """
    :param subset_xml_dir: first dataset (must be a subset of second one).
    :param full_xml_dir: second dataset.
    :return:
    """
    subset_doc_name2txt, subset_doc_name2anno = gen_anno_from_xml(subset_xml_dir, subset_dataset)
    full_doc_name2txt, full_doc_name2anno = gen_anno_from_xml(full_xml_dir, full_dataset)

    # make sure the all doc_name 


if __name__ == '__main__':
    pass