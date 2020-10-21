@echo off

for /F %%a in (.env) do (
	set %%a
)
rem echo %projname%
rem echo %appnames%


:start
echo on
pipenv run python %projname%/manage.py runserver

@echo off
echo.
echo -------------------------------
echo ! press any key to run again !
echo -------------------------------
pause >nul
goto start