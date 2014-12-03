#!/bin/bash

### Resources for each job

#PBS -t 1-500%45
#PBS -l walltime=12:00:00 
#PBS -l nodes=1:ppn=1
#PBS -j oe

# get current script directory
SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR == '.' ]
then
SCRIPT_DIR=$(pwd)
fi

#For debug
#PBS_ARRAYID=2
#SAMPLE_LEVEL=5 # set when submit job

#Default arguments
PROJECT_DIR=$(dirname "${SCRIPT_DIR}")
ROOT_INPUT_DIR="${PROJECT_DIR}/data/mxs"
ROOT_OUTPUT_DIR="${PROJECT_DIR}/data/output"
MAX_DEPTH=3
IMG_SIZE=128

# parse arguments
if [ $# == 5 ] 
then
  SAMPLE_LEVEL = $1
  ROOT_INPUT_DIR=$2
  ROOT_OUTPUT_DIR=$3
  MAX_DEPTH=$4
  IMG_SIZE=$5
fi


if [ -z "${SAMPLE_LEVEL}"] 
then
  echo "USAGE: ./pbs_render_all_mxs.sh [ <SL>  <ROOT_INPUT_DIR> <ROOT_OUTPUT_DIR> <MAX_DEPTH> <IMG_SIZE>]"
  exit -1
fi



CUR_MXS_FILE=`find ${ROOT_INPUT_DIR} -maxdepth $MAX_DEPTH -iname "*.mxs" | head -n ${PBS_ARRAYID} | tail -n 1`

# if ${CUR_MXS_FILE} not an empty string
if [ -n "${CUR_MXS_FILE}" ]
then
  MXS_NAME=$(basename "${CUR_MXS_FILE}")
  
  #get the path of current mxs file relative to the root_input
  CUR_INPUT_DIR=$(dirname "${CUR_MXS_FILE}")
  RELATIVE_PATH=${CUR_INPUT_DIR#${ROOT_INPUT_DIR}/}
  CUR_OUTPUT_DIR="${ROOT_OUTPUT_DIR}/${RELATIVE_PATH}"
  
  if [ ! -d "$CUR_OUTPUT_DIR" ]; then
    mkdir -p "$CUR_OUTPUT_DIR" 
  fi
 
  python "${SCRIPT_DIR}/render_one_mxs.py" "${CUR_MXS_FILE}" "${CUR_OUTPUT_DIR}" "${SAMPLE_LEVEL}" >> "${CUR_OUTPUT_DIR}/${MXS_NAME}.log"
fi
