#!/bin/bash

#$MXS_FILE=$1
#$OUTPUT_DIR=$2

FILE_NAME=$(basename "${MXS_FILE}")
NAME=${FILE_NAME%.*}
LOG_FILE="${OUTPUT_DIR}/${NAME}.log"

MXI_FILE="${OUTPUT_DIR}/${NAME}.mxi"
IMG_FILE="${OUTPUT_DIR}/${NAME}.png"
SL_DIR="${OUTPUT_DIR}/${NAME}"


#Render parameters
START_SL_LEVEL=22
FINAL_SL_LEVEL=30
SL_STEP=2
RESOLUTION="128x128"



echo "MXS_FILE       : ${MXS_FILE}         ">> $LOG_FILE
echo "START_SL_LEVLE : ${START_SL_LEVEL}   ">> $LOG_FILE
echo "FINAL_SL_LEVEL : ${FINAL_SL_LEVEL}   ">> $LOG_FILE
echo "OUTPUT_DIR     : ${OUTPUT_DIR}       ">> $LOG_FILE     # the output directory
echo "MXI_FILE       : ${MXI_FILE}         ">> $LOG_FILE
echo "IMG_FILE       : ${IMG_FILE}         ">> $LOG_FILE
echo "SL_DIR         : ${SL_DIR}           ">> $LOG_FILE
echo "RESOLUTION     : ${RESOLUTION}       ">> $LOG_FILE


#loading the maxwell module
module load maxwell
mkdir "$SL_DIR"

#iterate each sample level
for SL in $( seq $START_SL_LEVEL $SL_STEP $FINAL_SL_LEVEL) 
do
  #record start time
  START_TIME=$(date +%s) 
  
  #use maxwell render to render mxs 
  maxwell -nogui -nowait -trytoresume -mxs:"${MXI_FILE}" -res:$RESOLUTION -sl:$SL -mxi:"${MXI_FILE}" -output:"${IMG_FILE}" -dep:"/usr/local/maxwell-3.0/materials database/textures"
  
  #save current render result
  cp "${MXI_FILE}" "${SL_DIR}/${SL}.mxi"
  cp "${IMG_FILE}" "${SL_DIR}/${SL}.png"
  
  # record stop time
  END_TIEM=$(date +%s) 
  
  # compute render time 
  DIFF=$(( $END_TIME - $START_TIME ))
  
  # save the render time out 
  echo "$SL:$DIFF" >> $LOG_FILE
done
