cd %~dp0
call venv3/scripts/activate.bat

rem echo Mise a jour des add-ons
rem pip install -e add_ons

echo Lancement de Orange
orange-canvas

call venv3/scripts/deactivate.bat