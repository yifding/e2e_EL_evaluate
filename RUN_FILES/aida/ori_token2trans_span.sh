#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N ori_token2trans_span

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/aida/ori_token2trans_span.py
INPUT_DIR=/scratch365/yding4/EL_resource/data/raw/AIDA-CONLL
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/ori_token2trans_span


python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR}