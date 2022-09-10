from models import InvoiceHeaderData, InvoiceItem, Project
from utilities import objectToJson

project = Project(
    "Toggl To Invoice",
    100.0
)
invoiceItem = InvoiceItem(
    "0001",
    project,
    "Item 1",
    "A test item",
    1662836400,
    1662838200
)

def testInvoiceItemDuration():
    assert invoiceItem.durationInHours == 0.5, f"Expected 0.5, got {invoiceItem.durationInHours}"

def testInvoiceItemToJSON():
    invoiceItemJson = objectToJson(invoiceItem)
    expectedJson = '{"id": "0001", "project": {"name": "Toggl To Invoice", "ratePerHour": 100.0}, "title": "Item 1", "description": "A test item", "startTimeEpochInSeconds": 1662836400, "endTimeEpochInSeconds": 1662838200}'
    assert invoiceItemJson == expectedJson, f"""Expecting:
{expectedJson}
Got:
{invoiceItemJson}
"""

if __name__ == "__main__":
    testInvoiceItemDuration()
    testInvoiceItemToJSON()
    print("Done test_models")