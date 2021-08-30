#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N aida_xml_from_end2end_neural

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/end2end_neural_el/xml_from_end2end_neural_el.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/aida/xml/copy_xml_from_end2end_neural_el
DATASETS="['aida_testa','aida_testb','aida_train']"
URL="http://localhost:5555"

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS} --URL ${URL}