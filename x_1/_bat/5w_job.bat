@echo off
for /F %%a in (.env) do (
	set %%a
)
rem echo %projname%
rem echo %appnames%

echo on

pipenv run python %projname%/manage.py runapscheduler

pause
