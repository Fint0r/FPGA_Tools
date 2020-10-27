#!/bin/bash
# Get the directory the script is in
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# Location for the python virtual environment
ENV=$BASEDIR/fpgatools-venv
# Reading arguments
if [ "$1" == "clean" ]
then
  # Delete build directory
  rm -r "$BASEDIR/../build"
  # Delete pyinstaller's .spec file
  rm "$BASEDIR/../FPGA_Tools.spec"
  # Delete fpgatools-venv
  rm -r "$ENV"
  exit
elif [ "$1" == "" ]
then
  # Create python virtual environment
  echo "Creating python virtual environment..."
  python3 -m venv "$ENV"
  echo "Python virtual environment created"
  # Activate python virtual environment
  source "$ENV/bin/activate"
  # Check if we are in the right venv
  if [ "$(which python)" != "$ENV/bin/python" ]
  then
    echo "Error: Python virtual environment not activated!"
    exit 126
  else
    echo "Python virtual environment activated!"
  fi
  # Update pip
  python3 -m pip install --upgrade pip
  # install PyQt5 and pyinstaller in venv
  pip install PyQt5 pyinstaller
  # Create executable
  pyinstaller --onefile --noconsole --paths "$BASEDIR/../fpgatools" --distpath "$BASEDIR/../runnable exe" "$BASEDIR/../fpgatools/FPGA_Tools.py"
  # Exit python virtual environment
  deactivate
else
  echo "Usage:"
  echo "generate_linux.sh       - Builds FPGA_Tools."
  echo "generate_linux.sh clean - Deletes temporary files from the build process."
fi
