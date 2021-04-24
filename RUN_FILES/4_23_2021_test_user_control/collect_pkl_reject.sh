#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_collect_pkl_accept

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/process_db_data/collect_pkl.py

INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/4_23_2021/download_db2disk/reject
SOURCE_XML_DIR=/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL
REWRITE_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/4_23_2021/rewrite_xml/reject
LABEL_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/4_23_2021/label_xml/reject

python ${CODE} \
    --input_dir ${INPUT_DIR}    \
    --source_xml_dir    ${SOURCE_XML_DIR}   \
    --rewrite_xml_output_dir    ${REWRITE_XML_OUTPUT_DIR}   \
    --label_xml_output_dir  ${LABEL_XML_OUTPUT_DIR}