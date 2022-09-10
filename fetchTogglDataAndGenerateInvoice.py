import sys
import utilities

# CLI Args:
# python fetchDataAndGenerateInvoice.py {isDebug}
# isDebug: debug mode is ON if anything other than "0" or undefined is passed in.
# configToggleApiPath: path to configToggleApi.json
# configProjectsPath: path to configProjects.json

isDebug = sys.argv[1] != "0" if len(sys.argv) > 1 else False
configToggleApiPath = sys.argv[2] if len(sys.argv) > 2 else "configToggleApi.json"
configProjectsPath = sys.argv[3] if len(sys.argv) > 3 else "configProjects.json"

if isDebug:
    print("Debug mode on.")

def printDebug(message):
    if isDebug:
        print(message)

if __name__ == "__main__":
    printDebug("Fetching data from Toggl")

    configToggleApi = utilities.readJsonFromFile(configToggleApiPath)
    projects = utilities.readJsonFromFile(configProjectsPath)
    print(projects)

    printDebug("Generating template")

    