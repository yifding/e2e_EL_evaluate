#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N ori_xml2revise_xml

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/wned/ori_xml2revise_xml.py
INPUT_DIR=/scratch365/yding4/EL_resource/data/raw/wned-datasets
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/wned/xml/ori_xml2revise_xml
DATASETS="['ace2004','aquaint','clueweb','msnbc','wikipedia']"

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS}