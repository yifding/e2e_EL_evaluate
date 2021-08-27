#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_intersection_anno_agreement

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/process_db_data/intersection_anno_agreement.py

INTERSECT_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_xml_EL
SUBSET_ORI_XML_OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/5_20_2021/intersect_subset_xml_EL

python ${CODE}  \
    --intersect_xml_output_dir  ${INTERSECT_XML_OUTPUT_DIR} \
    --subset_ori_xml_output_dir ${SUBSET_ORI_XML_OUTPUT_DIR} \
    > intersection_anno_agreement.log