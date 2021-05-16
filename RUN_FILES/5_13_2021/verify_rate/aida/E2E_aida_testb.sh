#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N CRC_edit_entity_from_two_xml

export PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/bin:$PATH
export LD_LIBRARY_PATH=/afs/crc.nd.edu/user/y/yding4/.conda/envs/e2e_EL_evaluate/lib:$LD_LIBRARY_PATH

CODE=/scratch365/yding4/e2e_EL_evaluate/e2e_EL_evaluate/evaluation/obtain_verify_edit_entity_from_two_xml.py


python ${CODE}  \
    --subset_xml_dir    /scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/label_xml_EL \
    --full_xml_dir  /scratch365/yding4/e2e_EL_evaluate/data/5_13_2021/collect_pkl_rewrite_xml_EL   \
    --datasets  "['aida_testb']"    \
    --models    "['end2end_neural_el']"   > E2E_aida_testb.log

# --datasets  "['ace2004','aquaint','clueweb','msnbc','wikipedia','aida_testa','aida_testb','aida_train']"    \
# --models    "['GT','rel','end2end_neural_el']"