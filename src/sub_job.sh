#!/bin/bash

# Find the job script location
SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR == '.' ]
then
SCRIPT_DIR=$(pwd)
fi
FN_JOB_SCRIPT="${SCRIPT_DIR}/pbs_render_all_mxs.sh"

qsub -v SAMPLE_LEVEL=$1 ${FN_JOB_SCRIPT}