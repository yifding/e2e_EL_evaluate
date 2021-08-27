#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N wned_xml_from_end2end_neural

export PATH=/home/yding4/anaconda3/envs/hetseq/bin:$PATH
export LD_LIBRARY_PATH=/home/yding4/anaconda3/envs/hetseq/lib:$LD_LIBRARY_PATH

CODE=/home/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/end2end_neural_el/xml_from_end2end_neural_el.py
INPUT_DIR=/home/yding4/e2e_EL_evaluate/data/wned/xml/revise_xml2el_xml
OUTPUT_DIR=/home/yding4/e2e_EL_evaluate/data/wned/xml/xml_from_end2end_neural_el
DATASETS="['ace2004','aquaint','clueweb','msnbc','wikipedia']"
URL="http://localhost:5555"

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS} --URL ${URL}