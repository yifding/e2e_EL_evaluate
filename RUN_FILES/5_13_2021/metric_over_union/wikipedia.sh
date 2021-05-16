#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_wikipedia

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/process_db_data/union_of_verified_anno.py

MODEL_XML_DIR='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_subset_xml_EL'
INPUT_VERIFY_DIR='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_xml_EL'
DATASET='wikipedia'
METHOD='greedy'

python ${CODE}  \
    --model_xml_dir  ${MODEL_XML_DIR}   \
    --input_verify_dir  ${INPUT_VERIFY_DIR} \
    --dataset   ${DATASET} \
    --method    ${METHOD}   \
    > wikipedia.log


# --is_strong_match
# --dataset
# choices=['ace2004', 'aquaint', 'clueweb', 'msnbc', 'wikipedia', 'aida_testa', 'aida_testb', 'aida_train'],