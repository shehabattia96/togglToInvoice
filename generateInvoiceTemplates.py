from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import InvoiceHeaderData, InvoiceItem, Project
from utilities import objectToJson,epochToMMDDYYYYString, secondsToHours, secondsToHoursMinutesSeconds

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape()
)

invoiceTemplate = env.get_template("invoiceTemplate.j2")
invoiceItemsTemplate = env.get_template("invoiceItemsTemplate.j2")

def generateInvoiceFromHeaderAndItems(headerData:InvoiceHeaderData, allProjects:list, summedProjectDurationsInSeconds):


    summedProjectDurationsInHours = {}
    for projectId in summedProjectDurationsInSeconds:
        summedProjectDurationsInHours[projectId] = secondsToHours(summedProjectDurationsInSeconds[projectId])


    return invoiceTemplate.render(
        headerData=headerData,
        allProjects=allProjects,
        summedProjectDurationsInSeconds=summedProjectDurationsInSeconds,
        summedProjectDurationsInHours=summedProjectDurationsInHours,
        secondsToHoursMinutesSeconds=secondsToHoursMinutesSeconds
    )

def generateInvoiceReportDetailsFromItems(invoiceItems:list, allProjects:list):
    return invoiceItemsTemplate.render(
        allProjects=allProjects,
        invoiceItems=invoiceItems,
        epochToMMDDYYYYString=epochToMMDDYYYYString,
        secondsToHours=secondsToHours,
        secondsToHoursMinutesSeconds=secondsToHoursMinutesSeconds
    )