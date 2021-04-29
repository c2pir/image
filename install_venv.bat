cd %~dp0

py -m pip install --upgrade pip

rem install virtualenv and setuptools library
py -m pip install virtualenv
py -m pip install setuptools

rem create virtual env
py -m venv venv3

rem install packages on virtual env
call venv3/scripts/activate.bat
python -m pip install --upgrade pip
echo Mise a jour des add-ons
pip install -e add_ons

echo Fin de l'installation
call venv3/scripts/deactivate.bat