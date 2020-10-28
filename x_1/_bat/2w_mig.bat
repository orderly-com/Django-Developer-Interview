@echo off
for /F "delims=" %%a in (.env) do (
	set "%%a"
)
::echo %projname%
echo %appnames%

echo on
pipenv run python %projname%/manage.py makemigrations %appnames%
pipenv run python %projname%/manage.py migrate

pause