#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

source "$SCRIPT_DIR/sourceEnvironment.sh"

# See "CLI Args" in fetchTogglDataAndGenerateInvoice.py for info on args:
python "$SCRIPT_DIR/fetchTogglDataAndGenerateInvoice.py" "$@"