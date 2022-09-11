#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/
VENV_DIR="$SCRIPT_DIR/../venv"


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment"
    python -m venv "$VENV_DIR" || python3 -m venv "$VENV_DIR"
fi

SOURCE_DIR="$VENV_DIR/Scripts/activate"
if [ ! -d "$SOURCE_DIR" ]; then
    SOURCE_DIR="$VENV_DIR/bin/activate"
fi

source "$SOURCE_DIR"

echo "Installing pip dependencies"

pip install -r "$SCRIPT_DIR/requirements.txt"


echo "Done creating virtual environment and installing dependencies."