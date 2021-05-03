#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_collect_pkl_from_verified_anno

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/process_db_data/collect_pkl_from_verified_anno.py

INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_3_2021_investigation/download_db2disk
SOURCE_XML_DIR=/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL
REWRITE_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_3_2021_investigation/collect_pkl_rewrite_xml_EL
LABEL_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_3_2021_investigation/label_xml_EL

python ${CODE} \
    --input_dir ${INPUT_DIR}    \
    --source_xml_dir    ${SOURCE_XML_DIR}   \
    --rewrite_xml_output_dir    ${REWRITE_XML_OUTPUT_DIR}   \
    --label_xml_output_dir  ${LABEL_XML_OUTPUT_DIR}
