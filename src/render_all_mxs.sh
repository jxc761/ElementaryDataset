#!/bin/bash


SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR == '.' ]
then
SCRIPT_DIR=$(pwd)
fi


if [ $# == 3 ] 
then
  ROOT_INPUT_DIR=$1
  ROOT_OUTPUT_DIR=$2
  MAX_DEPTH=$3
  
else #debug
  echo "usage: ./render_all_mxs.sh <ROOT_INPUT_DIR> <ROOT_OUTPUT_DIR> <MAX_DEPTH>"
  echo "Run in default mode: "
  PROJECT_DIR=$(dirname "${SCRIPT_DIR}")
  ROOT_OUTPUT_DIR="${PROJECT_DIR}/data/output"
  ROOT_INPUT_DIR="${PROJECT_DIR}/data/mxs"
  MAX_DEPTH=3
  SAMPLE_LEVEL=24
  RESOLUTION="128x128"
fi

MXS_LIST="$(find ${ROOT_INPUT_DIR} -maxdepth $MAX_DEPTH -iname "*.mxs")"
for CUR_MXS_FILE in ${MXS_LIST}
do
  MXS_NAME=$(basename "${CUR_MXS_FILE}")
  
  #get the path of current mxs file relative to the root_input
  CUR_INPUT_DIR=$(dirname "${CUR_MXS_FILE}")
  RELATIVE_PATH=${CUR_INPUT_DIR#${ROOT_INPUT_DIR}/}
  CUR_OUTPUT_DIR="${ROOT_OUTPUT_DIR}/${RELATIVE_PATH}"
  
  # echo "OUTPUT_DIR    : ${CUR_OUTPUT_DIR}"
  # echo "MXS_FILE      : ${CUR_MXS_FILE}"
  # if $CUR_OUTPUT_DIR doesn't exist
  if [ ! -d "$CUR_OUTPUT_DIR" ]; then
    mkdir -p "$CUR_OUTPUT_DIR" 
  fi
 
  SYS_NAME=$(uname)
  if [ "${SYS_NAME}" == "Linux" ] # on hpc
  then
    
    # qsub -N "${MXS_NAME}" -l walltime=120:00:00 -l nodes=1:ppn=1 -v MXS_FILE=$CUR_MXS_FILE,OUTPUT_DIR=$CUR_OUTPUT_DIR "${SCRIPT_DIR}/progress_render_one_mxs.sh" -t 2800000-2810000%64
    qsub -N "${MXS_NAME}" -l walltime=120:00:00 -l nodes=1:ppn=1 -v MXS_FILE=$CUR_MXS_FILE,OUTPUT_DIR=$CUR_OUTPUT_DIR,SL=$SAMPLE_LEVEL,RES=$RESOLUTION "${SCRIPT_DIR}/render_one_mxs.sh"
    
  else
    # for debug
    "${SCRIPT_DIR}/progress_render_one_mxs.sh" "${CUR_MXS_FILE}" "${CUR_OUTPUT_DIR}"
    exit -2
  fi
 
done