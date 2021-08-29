#!/bin/bash

export PATH=/home/yding4/anaconda3/envs/hetseq/bin:$PATH
export LD_LIBRARY_PATH=/home/yding4/anaconda3/envs/hetseq/lib:$LD_LIBRARY_PATH

CODE=/home/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/rel/xml_from_rel.py
INPUT_DIR=/home/yding4/e2e_EL_evaluate/data/aida/xml/trans_span2el_span
OUTPUT_DIR=/home/yding4/e2e_EL_evaluate/data/has_prob/xml_from_rel
DATASETS="['aida_testa','aida_testb','aida_train']"
URL="http://127.0.0.1:1235"

python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS} --URL ${URL}  --has_prob