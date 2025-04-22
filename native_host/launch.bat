@echo off

:: Assumes native_bridge.py and the 'venv' folder are in the same directory as this batch file.

:: Path to venv python relative to this batch file
set VENV_PYTHON="%~dp0venv\Scripts\python.exe"

:: Path to the python script relative to this batch file
set SCRIPT_PATH="%~dp0native_bridge.py"

:: Define ONLY the stderr log file path
set STDERR_LOG="%~dp0native_bridge_stderr.log"

:: Standard output (>) is LEFT ALONE so the browser can read it.
%VENV_PYTHON% %SCRIPT_PATH% 2> %STDERR_LOG%