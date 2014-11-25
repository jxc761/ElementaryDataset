#!/bin/bash

# find itself location
SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR == '.' ]
then
SCRIPT_DIR=$(pwd)
fi

ROOT_DIR=$(dirname $SCRIPT_DIR)

# make clear output directories
DATA_DIR="${ROOT_DIR}/data"
if [ -d "${DATA_DIR}/studio" ]
then
  rm -r "${DATA_DIR}/studio"
fi
if [ -d "${DATA_DIR}/shootscript" ]
then  
  rm -r "${DATA_DIR}/shootscript"
fi
mkdir "${DATA_DIR}/studio"
mkdir "${DATA_DIR}/shootscript"

# run sketchup to generate scene and shootscripts
SU=`find /Applications -maxdepth 2 -iname Sketchup.app | head -1`
if [ "$SU" == "" ];then
   echo "Cannot find Sketchup. Please install Sketchup first..."
   exit
fi
RUBY_FILE="$SCRIPT_DIR/su.rb"

open --wait-apps "$SU"  --args -RubyStartup "${RUBY_FILE}"

