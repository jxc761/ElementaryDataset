#!/bin/bash

# Find the job script location
SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR == '.' ]
then
SCRIPT_DIR=$(pwd)
fi
FN_JOB_SCRIPT="${SCRIPT_DIR}/pbs_render_all_mxs.sh"
#FN_JOB_SCRIPT="${SCRIPT_DIR}/test_job.sh"

MIN_SL=24
SL_STEP=2
FINISH_SL=28
START_SL=`expr $MIN_SL + $SL_STEP`

# don't depend any other job
PRE_JOB_ID=`qsub -v SAMPLE_LEVEL=$MIN_SL ${FN_JOB_SCRIPT}` 

# sequentially render all scenes sl by sl
for CUR_SL in $(seq $START_SL $SL_STEP $FINISH_SL)
do
  # must run after the previous sl have been reached 
  CUR_JOB_ID=`qsub -W depend=afteranyarray:${PRE_JOB_ID} -v SAMPLE_LEVEL=$CUR_SL ${FN_JOB_SCRIPT}`
  PRE_JOB_ID=${CUR_JOB_ID}
done


