#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N step6

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE_DIR=/scratch365/yding4/e2e_EL_evaluate/baseline/deep_ed_PyTorch/deep_ed_PyTorch
DATA_PATH=/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data

python3 ${CODE_DIR}/data_gen/gen_wiki_data/gen_ent_wiki_w_repr.py --root_data_dir ${DATA_PATH}
python3 ${CODE_DIR}/data_gen/gen_wiki_data/gen_wiki_hyp_train_data.py --root_data_dir ${DATA_PATH}