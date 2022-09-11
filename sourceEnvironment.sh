#!/bin/sh

set -e

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

VENV_DIR="$SCRIPT_DIR/venv"


if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Did you run `sh ./development/createVirtualEnvAndInstallDependencies.sh`?"
    exit 1
fi


SOURCE_DIR="$VENV_DIR/Scripts/activate"
if [ ! -d "$SOURCE_DIR" ]; then
    SOURCE_DIR="$VENV_DIR/bin/activate"
fi


source "$SOURCE_DIR"
