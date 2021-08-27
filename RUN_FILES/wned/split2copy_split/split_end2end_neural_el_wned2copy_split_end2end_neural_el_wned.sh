#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N el_xml2copy_el_xml

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/wned/revise_xml2el_xml.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL/end2end_neural_el/wned
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/copy_EL/end2end_neural_el/wned
DATASETS="['ace2004','aquaint','clueweb','msnbc','wikipedia']"

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS}