#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N wned_xml_from_rel

export PATH=/home/yding4/anaconda3/envs/hetseq/bin:$PATH
export LD_LIBRARY_PATH=/home/yding4/anaconda3/envs/hetseq/lib:$LD_LIBRARY_PATH

CODE=/home/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/rel/xml_from_rel.py
INPUT_DIR=/home/yding4/e2e_EL_evaluate/data/wned/xml/revise_xml2el_xml
OUTPUT_DIR=/home/yding4/e2e_EL_evaluate/data/wned/xml/copy_xml_from_rel
DATASETS="['ace2004','aquaint','clueweb','msnbc','wikipedia']"
URL="http://127.0.0.1:1235"

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS} --URL ${URL}