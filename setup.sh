#!/bin/bash

echo INSTALLING VIRTUALENV WITH PIP\n
python3 -m pip install --user virtualenv # <- be sure to have python3 not python

echo PRINT YOUR CURRENT WORKING DIRECTORY\n
echo You are in $PWD

echo CREATING A DIRECTORY FOR THE VENV IN CURRENT DIRECTORY\n
mkdir virtualenvs

echo GOIN IN THE virtualenvs DIRECTORY\n
cd virtualenvs

echo CREATING A VENV FOR THE SCRIPT TO RUN IN WITH PYTHON3 RUNTIME\n
virtualenv -p python3 genenv

echo SWITCH BACK DIRECTORIES\n
cd ..

echo ACTIVATING THE NEWLY CREATED VENV(genenv)\n
. virtualenvs/genenv/bin/activate

echo INSTALLING DEPENDENCIES FOR THE SCRIPT FROM requirements.txt IN genenv\n
python3 -m pip install -r requirements.txt

echo READY TO RUN THE SCRIPT!