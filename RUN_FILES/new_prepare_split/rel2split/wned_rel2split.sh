#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N wned_rel2split

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/split_sentence/split_sentence.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/wned/xml/xml_from_rel
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/new_prepare_split/EL/rel/wned
DATASETS="['ace2004','aquaint','clueweb','msnbc','wikipedia']"
MAX_NUM_CHAR=300

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} \
    --datasets ${DATASETS} --max_num_char ${MAX_NUM_CHAR}