#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N aida_xml_from_end2end_neural

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH


CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/cleanlab/prepare_cleanlab_input.py

INTERSECT_XML_EL_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL/end2end_neural_el/aida
INTERSECT_SUBSET_XML_EL_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL/end2end_neural_el/aida
ORI_XML_EL_WITH_PROB_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/prepare_split/end2end_neural
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input/end2end_neural
DATASETS="['aida_testa','aida_testb','aida_train']"

python ${CODE}  \
    --intersect_xml_EL_dir ${INTERSECT_XML_EL_DIR}   \
    --intersect_subset_xml_EL_dir ${INTERSECT_SUBSET_XML_EL_DIR}  \
    --ori_xml_EL_with_prob_dir ${ORI_XML_EL_WITH_PROB_DIR}    \
    --output_dir ${OUTPUT_DIR}    \
    --datasets ${DATASETS}
