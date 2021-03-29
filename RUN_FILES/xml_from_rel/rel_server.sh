#!/bin/bash

#$-m abe
#$-M yding4@nd.edu
#$-q gpu # specify the queue
#$-l gpu_card=4
#$-N rel_server

export PATH=/home/nbotzer/el_venv/bin:$PATH
export LD_LIBRARY_PATH=/home/nbotzer/el_venv/lib:$LD_LIBRARY_PATH

CODE=/home/nbotzer/Github/EL_resource/baseline/REL/launch_REL_server.py

python ${CODE}