import sys
import utilities
import toggl
import togglModels
import models
import generateInvoiceTemplates

# CLI Args:
# python fetchDataAndGenerateInvoice.py {isDebug} {configToggleApiPath} {configProjectsPath} {configClientCompaniesPath} {startDateEpoch} {endDateEpoch}
# isDebug: debug mode is ON if anything other than "0" or undefined is passed in.
# configToggleApiPath: path to configToggleApi.json or similar
# configProjectsPath: path to configProjects.json or similar
# configClientCompaniesPath: path to configClientCompanies.json or similar
# startDateEpoch: get toggl time entries starting this date
# endDateEpoch: get toggl time entries up to (inclusive) this date
#
# for example:
# python fetchDataAndGenerateInvoice.py 1 "configToggleApi.json" "configProjects.json" "configClientCompanies.json" 0 0

isDebug = sys.argv[1] != "0" if len(sys.argv) > 1 else False
configToggleApiPath = sys.argv[2] if len(sys.argv) > 2 else "configToggleApi.json"
configProjectsPath = sys.argv[3] if len(sys.argv) > 3 else "configProjects.json"
configClientCompaniesPath = sys.argv[4] if len(sys.argv) > 4 else "configClientCompanies.json"
epochNow = utilities.epochNowInSeconds()
#Default to a week in the past
startDateEpoch = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "0" else epochNow - 60*60*24*7
endDateEpoch = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] != "0" else epochNow

if isDebug:
    print("Debug mode on.")

def printDebug(message):
    if isDebug:
        print(message)

if __name__ == "__main__":
    printDebug("Fetching data from Toggl")

    configToggleApi = utilities.readJsonFromFile(configToggleApiPath)


    # MARK: parse Companies from configClientCompaniesPath:
    allClientCompanies = utilities.readJsonFromFile(configClientCompaniesPath)
    
    clientCompaniesDict = {}
    for clientCompany in allClientCompanies:
        clientCompany = models.Company(**allClientCompanies[clientCompany])
        clientCompaniesDict[clientCompany.clientId] = clientCompany


    # MARK: parse Projects from configProjectsPath:
    allProjects = utilities.readJsonFromFile(configProjectsPath)

    projectsDict = {}
    clientProjectsDict = {} # the key is a clientId
    invoiceItemsDict = {}
    summedProjectDurationsInSeconds = {} # toggl project's actual_hours does not count minutes, so we'll sum timeEntries' duration here
    
    for project in allProjects:
        project = models.Project(**allProjects[project])
        projectsDict[project.id] = project
        invoiceItemsDict[project.id] = []
        summedProjectDurationsInSeconds[project.id] = 0

        clientId = project.clientId or "Unknown"
        if clientId not in clientCompaniesDict:
            clientId = "Unknown"
        
        if clientId not in clientProjectsDict:
            clientProjectsDict[clientId] = []

        clientProjectsDict[clientId].append(project.id)


    # MARK: parse InvoiceItems from a toggl http request:
    allTimeEntries = toggl.getAllTimeEntries(
        apiEndpoint=configToggleApi["apiEndpoint"],
        startDateEpoch=startDateEpoch,
        endDateEpoch=endDateEpoch,
        requestHeader=toggl.generateRequestHeader(apiToken=configToggleApi["apiToken"])
    )
    
    for timeEntry in allTimeEntries:
        invoiceItem:models.InvoiceItem = togglModels.mapTogglePayloadToInvoiceItem(**timeEntry)

        assert invoiceItem.projectId in invoiceItemsDict, f"Could not find project with id {invoiceItem.projectId} for timeEntry {invoiceItem.id}:{invoiceItem.description}"

        invoiceItemsDict[invoiceItem.projectId].append(invoiceItem)
        summedProjectDurationsInSeconds[invoiceItem.projectId] += invoiceItem.durationInSeconds



    summedProjectDurationsInHours = summedProjectDurationsInSeconds
    for projectId in summedProjectDurationsInSeconds:
        summedProjectDurationsInHours[projectId] = utilities.secondsToHours(summedProjectDurationsInHours[projectId])

    printDebug("Generating template for each client")

    for clientId in clientProjectsDict:
        clientProjects = clientProjectsDict[clientId]
        if clientId == "Unknown":
            printDebug(f"Skipping projects with unknown client: {utilities.objectToJson(clientProjects)}")
            continue

        client:models.Company = clientCompaniesDict[clientId]

        invoiceHeaderData = models.InvoiceHeaderData(
            invoicePreparedOnDate=utilities.epochToMMDDYYYYString(utilities.epochNowInSeconds()),
            invoiceNumber=1,
            invoiceStartDate=utilities.epochToMMDDYYYYString(startDateEpoch),
            invoiceEndDate=utilities.epochToMMDDYYYYString(endDateEpoch),
            fromCompany=clientCompaniesDict["0"],
            toCompany=client
        )

        allProjects = [projectsDict[projectId] for projectId in clientProjects]
        allInvoiceItems = []
        for projectId in clientProjects:
            allInvoiceItems += invoiceItemsDict[projectId]

        templateOutput = generateInvoiceTemplates.generateInvoiceFromHeaderAndItems(
            headerData=invoiceHeaderData,
            allProjects=allProjects,
            summedProjectDurationsInHours=summedProjectDurationsInHours
        )
        
        templateOutput += generateInvoiceTemplates.generateInvoiceReportDetailsFromItems(
            invoiceItems=allInvoiceItems,
            allProjects=allProjects
        )

        utilities.writeToFile(f"{clientId}_{startDateEpoch}_{endDateEpoch}.html", templateOutput)



    