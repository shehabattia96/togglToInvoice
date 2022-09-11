import sys
import utilities
import toggl
import togglModels
import models

# CLI Args:
# python fetchDataAndGenerateInvoice.py {isDebug} {configToggleApiPath} {configProjectsPath} {startDateEpoch} {endDateEpoch}
# isDebug: debug mode is ON if anything other than "0" or undefined is passed in.
# configToggleApiPath: path to configToggleApi.json or similar
# configProjectsPath: path to configProjects.json or similar
# startDateEpoch: get toggl time entries starting this date
# endDateEpoch: get toggl time entries up to (inclusive) this date
#
# for example:
# python fetchDataAndGenerateInvoice.py 1 "configToggleApi.json" "configProjects.json" 0 0

isDebug = sys.argv[1] != "0" if len(sys.argv) > 1 else False
configToggleApiPath = sys.argv[2] if len(sys.argv) > 2 else "configToggleApi.json"
configProjectsPath = sys.argv[3] if len(sys.argv) > 3 else "configProjects.json"
epochNow = utilities.epochNowInSeconds()
#Default to a week in the past
startDateEpoch = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "0" else epochNow - 60*60*24*7
endDateEpoch = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "0" else epochNow

if isDebug:
    print("Debug mode on.")

def printDebug(message):
    if isDebug:
        print(message)

if __name__ == "__main__":
    printDebug("Fetching data from Toggl")

    configToggleApi = utilities.readJsonFromFile(configToggleApiPath)
    allProjects = utilities.readJsonFromFile(configProjectsPath)
    
    header = toggl.generateRequestHeader(apiToken=configToggleApi["apiToken"])

    projectDict = {}
    invoiceItemsDict = {}
    summedProjectDurations = {} # toggl project's actual_hours does not count minutes, so we'll sum timeEntries' duration here
    
    for project in allProjects:
        project = models.Project(**allProjects[project])
        projectDict[project.id] = project
        invoiceItemsDict[project.id] = []
        summedProjectDurations[project.id] = 0


    allTimeEntries = toggl.getAllTimeEntries(
        apiEndpoint=configToggleApi["apiEndpoint"],
        startDateEpoch=startDateEpoch,
        endDateEpoch=endDateEpoch,
        requestHeader=header
    )
    

    for timeEntry in allTimeEntries:
        invoiceItem:models.InvoiceItem = togglModels.mapTogglePayloadToInvoiceItem(**timeEntry)

        assert invoiceItem.projectId in invoiceItemsDict, f"Could not find project with id {invoiceItem.projectId} for timeEntry {invoiceItem.id}:{invoiceItem.description}"

        invoiceItemsDict[invoiceItem.projectId].append(invoiceItem)
        summedProjectDurations[invoiceItem.projectId] += invoiceItem.durationInSeconds

    print(utilities.objectToJson(invoiceItemsDict, prettify=True))
    print(utilities.objectToJson(summedProjectDurations, prettify=True))

    printDebug("Generating template")

    