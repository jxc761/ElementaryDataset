#!/bin/bash

SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR == '.' ]
then
SCRIPT_DIR=$(pwd)
fi
PROJECT_DIR=$(dirname $SCRIPT_DIR)

OLD_PWD=$(pwd)

cd "${PROJECT_DIR}"

# clear local data file 
DATA_DIR="${PROJECT_DIR}/data"
rm -r "${DATA_DIR}/mxs"
rm -r "${DATA_DIR}/output"
rm -r "${DATA_DIR}/mxs_with_mxm"

SRC_DIR="${PROJECT_DIR}/src"
rm ${SRC_DIR}/*.pyc

echo $DATA_DIR
echo $SRC_DIR

FN_TAR=$(date '+exp%Y%m%d.tar.gz')
tar czf "./${FN_TAR}" "./src/" "./data/"


scp "${PROJECT_DIR}/${FN_TAR}" jxc761@hpcviz.case.edu:~/
scp $SRC_DIR/run_maxwell_on_hpc.sh jxc761@hpcviz.case.edu:~/

rm "./${FN_TAR}"

cd "${OLD_PWD}"