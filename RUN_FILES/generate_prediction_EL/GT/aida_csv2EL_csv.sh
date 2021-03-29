#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N wned_csv2EL_csv

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/baseline/GT/clean_xml2EL_csv.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/processed/AIDA-CONLL/ori2xml
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/prediction/EL/GT/aida
DATASETS="['aida_testa','aida_testb','aida_train']"


python ${CODE} --input_dir ${INPUT_DIR} --output_dir ${OUTPUT_DIR} --datasets ${DATASETS}