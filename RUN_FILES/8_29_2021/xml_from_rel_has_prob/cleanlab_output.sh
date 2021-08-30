#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=1
#$-N prepare_cleanlab_aida

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH


CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/cleanlab/generate_cleanlab_ouput.py

INTERSECT_XML_EL_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL/rel/aida
INTERSECT_SUBSET_XML_EL_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL/rel/aida
ORI_XML_EL_WITH_PROB_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/prepare_split/rel
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input/rel
DATASETS="['aida_testa','aida_testb','aida_train']"

python ${CODE}  \
    --intersect_xml_EL_dir ${INTERSECT_XML_EL_DIR}   \
    --intersect_subset_xml_EL_dir ${INTERSECT_SUBSET_XML_EL_DIR}  \
    --ori_xml_EL_with_prob_dir ${ORI_XML_EL_WITH_PROB_DIR}    \
    --output_dir ${OUTPUT_DIR}    \
    --datasets ${DATASETS}
