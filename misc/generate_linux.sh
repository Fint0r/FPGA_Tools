#!/bin/sh
# Get the directory the script is in
BASEDIR=$(dirname $0)
# Create executable
pyinstaller --onefile --noconsole --paths $BASEDIR/../src --distpath $BASEDIR/../runnable\ exe $BASEDIR/../src/FPGA_Tools.py
# Delete build directory
rm -r $BASEDIR/../build
# Delet pyinstaller's .spec file
rm $BASEDIR/../*.spec
