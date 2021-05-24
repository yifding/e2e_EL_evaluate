#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_GT_over_union

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/process_db_data/GT_over_union_of_verified_anno.py

INPUT_VERIFY_DIR='/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL'
MODEL_XML_DIR='/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL'
MODELS="['GT']"

python ${CODE}  \
    --input_verify_dir  ${INPUT_VERIFY_DIR} \
    --model_xml_dir ${MODEL_XML_DIR}    \
    --models    ${MODELS}   \
    > GT_over_union.log
