#!/bin/sh

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

source "$SCRIPT_DIR/sourceEnvironment.sh"

isDebug=$1
configToggleApiPath=$2
configProjectsPath=$3
startDateEpoch=$4
endDateEpoch=$5

# See "CLI Args" in fetchTogglDataAndGenerateInvoice.py for info on args:
python "$SCRIPT_DIR/fetchTogglDataAndGenerateInvoice.py" ${isDebug:-0} ${configToggleApiPath:-configToggleApi.json} ${configProjectsPath:-configProjects.json} ${startDateEpoch:-0} ${endDateEpoch:-0}