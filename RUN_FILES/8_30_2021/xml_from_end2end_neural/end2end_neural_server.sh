#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N end2end_neural_EL_server

export PATH=/afs/crc.nd.edu/user/y/yding4/TF-1.4/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/TF-1.4/lib:$LD_LIBRARY_PATH

DIR=/scratch365/yding4/e2e_EL_evaluate/baseline/end2end_neural_el/code

cd ${DIR}
python -m gerbil.server --training_name=base_att_global --experiment_name=paper_models \
    --persons_coreference_merge=True --all_spans_training=True --entity_extension=extension_entities

