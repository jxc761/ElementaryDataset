#!/bin/bash

ROOT_INPUT_DIR=$1
ROOT_OUTPUT_DIR=$2
DEPTH=$3

# for debug
# ROOT_OUTPUT_DIR="/Users/Jing/Dropbox/3DMotion/ElementaryDataset/output"
# ROOT_INPUT_DIR="/Users/Jing/Dropbox/3DMotion/ElementaryDataset"
# DEPTH=2

for CUR_MXS_FILE in $(find "${ROOT_INPUT_DIR}" -depth $DEPTH -name *.mxs)
do
  #get the relative path of current mxs file to the root_input
  CUR_INPUT_DIR=$(dirname $CUR_MXS_FILE)
  REL_PATH=${CUR_INPUT_DIR#${ROOT_INPUT_DIR}/}

  CUR_OUTPUT_DIR="${ROOT_OUTPUT_DIR}/${REL_PATH}"
  
  # if $CUR_OUTPUT_DIR doesn't exist.
  if [ ! -d "$CUR_OUTPUT_DIR" ]; then
    mkdir -p "$CUR_OUTPUT_DIR" 
  fi
  
  
  echo "$CUR_OUTPUT_DIR"
  echo "$CUR_MXS_FILE"
  
  # qsub -N "${MXS_NAME}"  -l walltime=96:00:00 -l nodes=1:ppn=1 -v MXS_FILE=$CUR_MXS_FILE,OUTPUT_DIR=$CURRENT_OUTPUT_DIR ./progress_render_one_mxs.sh
  
done