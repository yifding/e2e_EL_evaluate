#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N aida_xml_from_end2end_neural

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/prepare_data/cleanlab/calibration_plots.py
INPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/cleanlab_input/rel
OUTPUT_DIR=/scratch365/yding4/e2e_EL_evaluate/data/has_prob/calibration_plots/rel
OUTPUT_FILE=rel.csv
DATASETS="['aida_testa','aida_testb','aida_train','ace2004','aquaint','clueweb','msnbc','wikipedia']"
NUM_BIN=10

python ${CODE}  \
  --input_dir ${INPUT_DIR}    \
  --output_dir ${OUTPUT_DIR}  \
  --output_file ${OUTPUT_FILE}    \
  --datasets ${DATASETS}    \
  --num_bin ${NUM_BIN}