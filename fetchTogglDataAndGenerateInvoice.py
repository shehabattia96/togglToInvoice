import sys
import argparse
import utilities
import toggl
import togglModels
import models
import generateInvoiceTemplates

parser=argparse.ArgumentParser()

# MARK: CLI Args:
parser.add_argument("invoiceNumber", help="Invoice Number")
epochNow = utilities.epochNowInSeconds()
parser.add_argument("--invoicePreparedOnDate", help="The date to display in the invoice as the invoice date.", default=utilities.epochToMMDDYYYYString(epochNow))
parser.add_argument("--startDateEpoch", help="Epoch to filter Toggl time entries' start date. Max 3 months. Defaults to 1 week ago.", default=epochNow - 60*60*24*7)
parser.add_argument("--endDateEpoch", help="Epoch to filter Toggl time entries' end date. Max 3 months. Defaults to now.", default=epochNow)
parser.add_argument("--isDebug", help="Displays debug messages.", default=False)
parser.add_argument("--configToggleApiPath", help="Path to configToggleApi.json or similar", default="configToggleApi.json")
parser.add_argument("--configProjectsPath", help="Path to configProjects.json or similar", default="configProjects.json")
parser.add_argument("--configClientCompaniesPath", help="Path to configClientCompanies.json or similar", default="configClientCompanies.json")

args=parser.parse_args().__dict__

[
    invoiceNumber,
    invoicePreparedOnDate,
    startDateEpoch,
    endDateEpoch,
    isDebug,
    configToggleApiPath,
    configProjectsPath,
    configClientCompaniesPath
] = [
        args[key] for key in 
            [
                "invoiceNumber",
                "invoicePreparedOnDate",
                "startDateEpoch",
                "endDateEpoch",
                "isDebug",
                "configToggleApiPath",
                "configProjectsPath",
                "configClientCompaniesPath"
            ]
]

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
            invoicePreparedOnDate=invoicePreparedOnDate,
            invoiceNumber=invoiceNumber,
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



    