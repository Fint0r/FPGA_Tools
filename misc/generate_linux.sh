#!/bin/sh
# Get the directory the script is in
BASEDIR=$(dirname $0)
# Activate the python virtual environment
source $BASEDIR/../pyvenv/bin/activate
# Create executable
pyinstaller --onefile --noconsole --paths $BASEDIR/../src --distpath $BASEDIR/../runnable\ exe $BASEDIR/../src/FPGA_Tools.py
# Deactivate the python virtual environment
deactivate
# Delete build directory
rm -r $BASEDIR/../build
# Delet pyinstaller's .spec file
rm $BASEDIR/../*.spec
