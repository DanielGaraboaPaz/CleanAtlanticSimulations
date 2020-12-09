@echo off
cls

call activate MOHID-Lagrangian

rem 
call ../MOHIDLagrangianPath.bat

rem "name" and "dirout" are named according to the case
set name=%cd%_case

rem "executables" are renamed and called from their directory
if "%dirout%"=="" (set dirout=%name%_out) else (set dirout=%dirout%%name%_out)ory

set postProcessorDir=../../src\MOHIDLagrangianPostProcessor
set postProcessor="%postProcessorDir%/MOHIDLagrangianPostprocessor.py"

python -W ignore %postProcessor% -i %name%.xml -o %dirout% -po

:success
echo All done
goto end

:fail
echo Execution aborted.

:end
pause
