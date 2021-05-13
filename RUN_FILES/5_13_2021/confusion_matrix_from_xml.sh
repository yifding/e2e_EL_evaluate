#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_intersection_verified_anno

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/evaluation/confusion_matrix_from_xml.py

MODEL_XML_DIR='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_xml_EL'
GT_XML_DIR='/scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/intersect_xml_EL'
MODEL_MODEL='end2end_neural_el'
GT_MODEL='GT'
DATASET='aida_testa'

python ${CODE}  \
    --model_xml_dir ${MODEL_XML_DIR}    \
    --GT_xml_dir    ${GT_XML_DIR} \
    --model_model   ${MODEL_MODEL}  \
    --GT_model  ${GT_MODEL} \
    --dataset   ${DATASET}  \
    --is_strong_match