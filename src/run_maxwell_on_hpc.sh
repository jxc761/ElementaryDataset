#!/bin/bash
echo ${HOME}

FN_TAR=$(date '+exp%Y%m%d.tar.gz')
EXP_DIR="${HOME}/"$(date '+exp%Y%m%d')

#prepare exp directory
echo ${EXP_DIR}
if [ -d "${EXP_DIR}" ]
then
  rm -r "${EXP_DIR}"
fi
mkdir "${EXP_DIR}"


OLD_PWD=$(pwd)
cd "${EXP_DIR}"
echo $(pwd)

tar xf "${HOME}/${FN_TAR}"

# prepare lib
LIB_DIR="${EXP_DIR}/lib" 
if [ ! -d "${LIB_DIR}" ]
then
  cp -r "${HOME}/lib" "${EXP_DIR}" 
fi


cd "${EXP_DIR}/src"
echo "Begin to build mxs files"
python "./maxwell.py"
echo "Finsh build mxs files"
#echo "Begin to render"
#./sequentially_render_all_mxs.sh

rm "${HOME}/${FN_TAR}"
cd "${OLD_PWD}"
