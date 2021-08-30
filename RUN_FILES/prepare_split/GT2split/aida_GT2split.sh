#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N aida_GT2split

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/split_sentence/split_sentence.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/prepare_split/EL/GT/aida
DATASETS="['aida_testa','aida_testb','aida_train']"
MAX_NUM_CHAR=300
MIN_NUM_CHAR=100

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} \
    --datasets ${DATASETS} --max_num_char ${MAX_NUM_CHAR}   --min_num_char ${MIN_NUM_CHAR}