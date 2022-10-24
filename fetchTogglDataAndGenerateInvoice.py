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
parser.add_argument("--invoicePreparedOnDateEpoch", help="The date epoch to display in the invoice as the invoice date.", default=epochNow, type=int)
parser.add_argument("--startDateEpoch", help="Epoch to filter Toggl time entries' start date. Max 3 months from endDateEpoch. Defaults to 1 week ago.", default=epochNow - 60*60*24*7, type=int)
parser.add_argument("--endDateEpoch", help="Epoch to filter Toggl time entries' end date. Defaults to now.", default=epochNow, type=int)
parser.add_argument("--hideProjectsWithNoHours", help="Projects that do not have hours are hidden.", default=False, action='store_true')
parser.add_argument("--hideDebugMessages", help="Hides debug messages.", default=False, action='store_true')
parser.add_argument("--configToggleApiPath", help="Path to configToggleApi.json or similar", default="configToggleApi.json")
parser.add_argument("--configProjectsPath", help="Path to configProjects.json or similar", default="configProjects.json")
parser.add_argument("--configClientCompaniesPath", help="Path to configClientCompanies.json or similar", default="configClientCompanies.json")

args=parser.parse_args().__dict__

# This is a landmine waiting to explode. Make sure to match the key unpacking order:
[
    invoiceNumber,
    invoicePreparedOnDateEpoch,
    startDateEpoch,
    endDateEpoch,
    hideProjectsWithNoHours,
    hideDebugMessages,
    configToggleApiPath,
    configProjectsPath,
    configClientCompaniesPath
] = [
        args[key] for key in 
            [
                "invoiceNumber",
                "invoicePreparedOnDateEpoch",
                "startDateEpoch",
                "endDateEpoch",
                "hideProjectsWithNoHours",
                "hideDebugMessages",
                "configToggleApiPath",
                "configProjectsPath",
                "configClientCompaniesPath"
            ]
]

if not hideDebugMessages:
    print("Debug mode on.")

def printDebug(message):
    if not hideDebugMessages:
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
        # toggl api only works with dates, so to get entries on the day of the epoch, you need to go a day in the future. We'll filter excess entries later:
        endDateEpoch=endDateEpoch+24*60*60,
        requestHeader=toggl.generateRequestHeader(apiToken=configToggleApi["apiToken"])
    )
    
    for timeEntry in allTimeEntries:
        invoiceItem:models.InvoiceItem = togglModels.mapTogglePayloadToInvoiceItem(**timeEntry)

        assert invoiceItem.projectId in invoiceItemsDict, f"Could not find project with id {invoiceItem.projectId} for timeEntry {invoiceItem.id}:{invoiceItem.description}"

        if invoiceItem.startTimeEpochInSeconds < startDateEpoch:
            print(f"Entry {invoiceItem.id} is before the startDateEpoch, skipping it.")
            continue

        if invoiceItem.startTimeEpochInSeconds > endDateEpoch:
            print(f"Entry {invoiceItem.id} is after the endDateEpoch, skipping it.")
            continue

        invoiceItemsDict[invoiceItem.projectId].append(invoiceItem)
        summedProjectDurationsInSeconds[invoiceItem.projectId] += invoiceItem.durationInSeconds

    printDebug("Generating an invoice for each client")

    fromCompany = clientCompaniesDict["0"]

    assert fromCompany, f"Client with clientId == 0 not found. Please add your name/company to {configClientCompaniesPath}."

    for clientId in clientProjectsDict:
        clientProjects = clientProjectsDict[clientId]
        if clientId == "Unknown":
            printDebug(f"Skipping projects with unknown client: {utilities.objectToJson(clientProjects)}")
            continue
        
        client:models.Company = clientCompaniesDict[clientId]

        outputFileName = f"Invoice #{invoiceNumber} - {utilities.epochToBDDYYYYString(invoicePreparedOnDateEpoch)} - {client.clientName} - {fromCompany.clientName}.html"
        
        printDebug(f"Generating {outputFileName}")

        invoiceHeaderData = models.InvoiceHeaderData(
            invoicePreparedOnDate=utilities.epochToMMDDYYYYString(invoicePreparedOnDateEpoch),
            invoiceNumber=invoiceNumber,
            invoiceStartDate=utilities.epochToMMDDYYYYString(startDateEpoch),
            invoiceEndDate=utilities.epochToMMDDYYYYString(endDateEpoch),
            fromCompany=fromCompany,
            toCompany=client
        )

        allProjects = []
        allInvoiceItems = []
        for projectId in clientProjects:
            allInvoiceItems += invoiceItemsDict[projectId]

            if hideProjectsWithNoHours:
                if summedProjectDurationsInSeconds[projectId] == 0:
                    continue

            allProjects.append(projectsDict[projectId])

        templateOutput = generateInvoiceTemplates.generateInvoiceFromHeaderAndItems(
            headerData=invoiceHeaderData,
            allProjects=allProjects,
            summedProjectDurationsInSeconds=summedProjectDurationsInSeconds
        )
        
        templateOutput += generateInvoiceTemplates.generateInvoiceReportDetailsFromItems(
            invoiceItems=allInvoiceItems,
            allProjects=allProjects
        )

        utilities.writeToFile(outputFileName, templateOutput)



    