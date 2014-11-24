#!/bin/bash

# find itself location
SCRIPT_DIR=$(dirname $0)
if [ $SCRIPT_DIR = '.' ]
then
SCRIPT_DIR=$(pwd)
fi

ROOT_DIR=$(dirname $SCRIPT_DIR)

DATA_DIR="${ROOT_DIR}/data"
rm -r "${DATA_DIR}/studio"
rm -r "${DATA_DIR}/shootscript"
mkdir "${DATA_DIR}/studio"
mkdir "${DATA_DIR}/shootscript"

# run sketchup to generate scene and shootscripts
SU=`find /Applications -maxdepth 2 -iname Sketchup.app | head -1`
if [ "$SU" == "" ];then
   echo "Cannot find Sketchup. Please install Sketchup first..."
   exit
fi
RUBY_FILE="${ROOT_DIR}/su.rb"

open --wait-apps "$SU"  --args -RubyStartup "${RUBY_FILE}"

# use pymaxwell to generate scenes with different materials 
# python ./maxwell.py

#upload data to hpc

#render all scenes

