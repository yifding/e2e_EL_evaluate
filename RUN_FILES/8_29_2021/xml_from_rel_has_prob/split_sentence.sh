#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N rel2split

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/split_sentence/split_sentence.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/xml_from_rel
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/prepare_split/rel
DATASETS="['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']"
MAX_NUM_CHAR=300
MIN_NUM_CHAR=100

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --has_prob \
    --datasets ${DATASETS} --max_num_char ${MAX_NUM_CHAR}   --min_num_char ${MIN_NUM_CHAR}