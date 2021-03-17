#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N train_local

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/baseline/deep_ed_PyTorch/deep_ed_PyTorch/ed/train.py

python ${CODE}  --model_type 'local'  --max_epoch 400 --train_file "aida_train_clean.csv" \
    --ent_vecs_filename 'ent_vecs__ep_12.pt' --top_ctxt_words 50  \
    --datasets "['aida_testa', 'aida_testb', 'msnbc', 'aquaint', 'ace2004', 'aida_train', 'clueweb', 'wikipedia']" \
    --root_data_dir "/scratch365/yding4/e2e_EL_evaluate/data/deep_ed_PyTorch_data"

