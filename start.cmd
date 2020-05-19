@echo off

echo Starting the processes to automate the illumination...

start /B py %CD%"\main_general.py" "-r" "kitchen"
start /B py %CD%"\main_general.py" "-r" "bedroom"
start /B py %CD%"\main_general.py" "-r" "livroom"

set /p train=Do you want to obtain training images before launching the process to control de smartTV? (Y/N):

IF "%train%"=="Y" (
	echo Starting autocapture process...
	start /wait py  %CD%"\auto_capture.py" "-i" "192.168.7.226" "-p" "8895"

	echo Starting the process to control the smartTV...
	start /B py  %CD%"\main_tv.py" "-i" "192.168.7.226" "-p" "8895" 
) ELSE (
	echo Starting the process to control the smartTV...
	start /B py  %CD%"\main_tv.py" "-i" "192.168.7.226" "-p" "8895"
)

pause