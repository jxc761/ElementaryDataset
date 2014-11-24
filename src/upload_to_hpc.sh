#!/bin/bash

SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR = '.' ]
then
SCRIPT_DIR=$(pwd)
fi
ROOT_DIR=$(dirname $SCRIPT_DIR)

OLD_PWD=$(pwd)

cd $ROOT_DIR

DATA_DIR="./data/"
SRC_DIR="./src"
echo $DATA_DIR
echo $SRC_DIR

FN_TAR=$(date '+exp%Y%m%d.tar.gz')
tar czf "${ROOT_DIR}/FN_TAR" $DATA_DIR $SRC_DIR


scp "${ROOT_DIR}/FN_TAR" jxc761@hpcviz.case.edu:~/

ssh jxc761@hpcviz.case.edu

tar xf "${FN_TAR}"
exit
cd "$OLD_PWD"