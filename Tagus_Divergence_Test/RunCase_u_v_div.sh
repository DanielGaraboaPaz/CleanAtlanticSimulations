#!/bin/bash
set -x
clear

# increase stacksize
ulimit -s unlimited
export KMP_STACKSIZE=1G

# Read the MOHIDLagrangianPath
source ../MOHIDLagrangianPath.sh

# "name" and "dirout" are named according to the testcase
name=u_v_w_case
#if no dirout is provided, create on local

if [ -z ${dirout+x} ]; 
then 
    dirout=${name}_out
else 
    dirout=${dirout}${name}_out
fi

# "executables" are renamed and called from their directory
tools=${MOHIDLagrangianPath}/build/bin
mohidlagrangian=${tools}/MOHIDLagrangian

preprocessorDir=${MOHIDLagrangianPath}/src/MOHIDLagrangianPreProcessor
mohidPreprocessor=${preprocessorDir}/MOHIDLagrangianPreProcessor.py

postProcessorDir=${MOHIDLagrangianPath}/src/MOHIDLagrangianPostProcessor
mohidPostprocessor=${postProcessorDir}/MOHIDLagrangianPostProcessor.py

# "dirout" is created to store results or it is cleaned if it already exists
if [ -e $dirout ]; then
  rm -f -r $dirout
fi
mkdir -p $dirout

cp ${name}.xml $dirout/

# CODES are executed according the selected parameters of execution in this testcase

python $mohidPreprocessor -i $dirout/${name}.xml -o $dirout

errcode=0
if [ $errcode -eq 0 ]; then
  $mohidlagrangian -i $dirout/${name}.xml -o $dirout
  errcode=$?
fi

python -W ignore $mohidPostprocessor -i ${name}.xml -o $dirout

if [ $errcode -eq 0 ]; then
  echo All done
else
  echo Execution aborted
fi
read -n1 -r -p "Press any key to continue..." key
echo
