from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import InvoiceHeaderData, InvoiceItem, Project
from utilities import objectToJson

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape()
)

invoiceTemplate = env.get_template("invoiceTemplate.j2")
invoiceItemsTemplate = env.get_template("invoiceItemsTemplate.j2")

def generateInvoiceFromHeaderAndItems(headerData:InvoiceHeaderData, allProjects:list, summedProjectDurationsInHours):
    # headerData = objectToJson(headerData)
    # allProjects = objectToJson(allProjects)
    print(headerData,allProjects, summedProjectDurationsInHours)
    return invoiceTemplate.render(
        headerData=headerData,
        allProjects=allProjects,
        summedProjectDurationsInHours=summedProjectDurationsInHours
    )

def generateInvoiceReportDetailsFromItems(invoiceItems:list):
    pass