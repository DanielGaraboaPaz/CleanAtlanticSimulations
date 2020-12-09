#!/bin/bash

clear

# Read the MOHIDLagrangianPath
source ../MOHIDLagrangianPath.sh

# "name" and "dirout" are named according to the testcase
name=${PWD##*/}_case

if [ -z ${dirout+x} ]; 
then 
    dirout=${name}_out
else 
    dirout=${dirout}${name}_out
fi

if [ -z ${dirout+x} ]; 
then 
    dirout=${name}_out
else 
    dirout=${dirout}${name}_out
fi


# "executables" are renamed and called from their directory

postProcessorDir=${MOHIDLagrangianPath}/src/MOHIDLagrangianPostProcessor
postProcessor=${postProcessorDir}/MOHIDLagrangianPostProcessor.py

# CODES are executed according the selected parameters of execution in this testcase
errcode=0

python -W ignore $postProcessor -i ${name}.xml -o $dirout -po

if [ $errcode -eq 0 ]; then
  echo All done
else
  echo Execution aborted
fi
read -n1 -r -p "Press any key to continue..." key
echo
