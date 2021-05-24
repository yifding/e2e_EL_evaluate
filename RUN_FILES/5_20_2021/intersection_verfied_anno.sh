#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_intersection_verified_anno

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/process_db_data/intersection_verfied_anno.py
REWRITE_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/collect_pkl_rewrite_xml_EL
LABEL_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/label_xml_EL
INTERSECT_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL
SUBSET_ORI_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL

python ${CODE}  \
    --rewrite_xml_output_dir    ${REWRITE_XML_OUTPUT_DIR}   \
    --label_xml_output_dir  ${LABEL_XML_OUTPUT_DIR}     \
    --intersect_xml_output_dir  ${INTERSECT_XML_OUTPUT_DIR}     \
    --subset_ori_xml_output_dir     ${SUBSET_ORI_XML_OUTPUT_DIR}