#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N step8

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE_DIR=/scratch365/yding4/e2e_EL_evaluate/baseline/deep_ed_PyTorch/deep_ed_PyTorch
DATA_PATH=/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data

python3 ${CODE_DIR}/entities/relatedness/filter_wiki_canonical_words_RLTD.py --root_data_dir ${DATA_PATH}
python3 ${CODE_DIR}/entities/relatedness/filter_wiki_hyperlink_contexts_RLTD.py --root_data_dir ${DATA_PATH}
