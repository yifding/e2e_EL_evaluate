#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_download_db_data

export PATH=/home/yding4/miniconda3/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/home/yding4/miniconda3/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/home/yding4/e2e_EL_evaluate/e2e_EL_evaluate/collect_data_from_db/download_db2disk.py
OUTPUT_DIR=/home/yding4/e2e_EL_evaluate/data/5_8_2021_analysis/download_db2disk

python ${CODE}  \
    --output_dir    ${OUTPUT_DIR}