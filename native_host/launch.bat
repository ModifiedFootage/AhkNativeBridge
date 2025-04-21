@echo off

:: Assumes native_bridge.py and the 'venv' folder are in the same directory as this batch file.

:: Path to venv python relative to this batch file
set VENV_PYTHON="%~dp0venv\Scripts\python.exe"

:: Path to the python script relative to this batch file
set SCRIPT_PATH="%~dp0native_bridge.py"

:: Define log file paths relative to this batch file's location
set STDOUT_LOG="%~dp0native_bridge_stdout.log"
set STDERR_LOG="%~dp0native_bridge_stderr.log"

:: Execute the script using the venv's python, redirecting output
%VENV_PYTHON% %SCRIPT_PATH% > %STDOUT_LOG% 2> %STDERR_LOG%