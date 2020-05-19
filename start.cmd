@echo off

echo Starting the processes to automate the illumination...

python C:\Users\Manuel\GitRepos\TFGSmarhome\main_general.py -r kitchen
python C:\Users\Manuel\GitRepos\TFGSmarhome\main_general.py -r bedroom
python C:\Users\Manuel\GitRepos\TFGSmarhome\main_general.py -r livroom

set /p train=Do you want to obtain training images before launching the process to control de smartTV? (Y/N):

IF "%train%"=="Y" (
	python C:\Users\Manuel\GitRepos\TFGSmarhome\auto_capture.py -i 192.168.7.226 -p 8895
)

python C:\Users\Manuel\GitRepos\TFGSmarhome\main_tv.py -i 192.168.7.226 -p 8895

pause