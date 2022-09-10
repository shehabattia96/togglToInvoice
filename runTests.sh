#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

source "$SCRIPT_DIR/sourceEnvironment.sh"

python -m tests.test_models
python -m tests.test_utilities