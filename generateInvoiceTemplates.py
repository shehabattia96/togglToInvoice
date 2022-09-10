from jinja2 import Environment, PackageLoader, select_autoescape
from models import InvoiceHeaderData, InvoiceItem

env = Environment(
    loader=PackageLoader("togglToInvoice"),
    autoescape=select_autoescape()
)

invoiceTemplate = env.get_template("invoiceTemplate.j2")
invoiceItemsTemplate = env.get_template("invoiceItemsTemplate.j2")

def generateInvoiceFromHeaderAndItems(invoiceHeader:InvoiceHeaderData, invoiceItems:list[InvoiceItem]):
    pass

def generateInvoiceReportDetailsFromItems(invoiceItems:list[InvoiceItem]):
    pass