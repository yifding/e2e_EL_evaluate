#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N eval_ent_embedding

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE_DIR=/scratch365/yding4/e2e_EL_evaluate/baseline/deep_ed_PyTorch/deep_ed_PyTorch
DATA_PATH=/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data

CODE=/scratch365/yding4/e2e_EL_evaluate/baseline/deep_ed_PyTorch/deep_ed_PyTorch

python ${CODE}/entities/learn_e2v/YD_eval_entity_embedding.py   --dir ${DATA_PATH}/generated/ent_vecs   \
    --root_data_dir ${DATA_PATH}

# python ${CODE} > final_test_output.txt
