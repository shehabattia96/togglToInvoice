from models import InvoiceHeaderData, InvoiceItem, Project
from utilities import objectToJson, secondsToHours

project = Project(
    id="0001",
    name="Toggl To Invoice",
    hourlyRate=100.0,
    billable=True,
    clientId=""
)
invoiceItem = InvoiceItem(
    id="0001",
    projectId=project.id,
    description="A test item",
    billable=False,
    startTimeEpochInSeconds=1662836400,
    endTimeEpochInSeconds=1662838200,
    durationInSeconds=1662838200-1662836400
)

def testInvoiceItemDuration():
    assert secondsToHours(invoiceItem.durationInSeconds) == 0.5, f"Expected 0.5, got {invoiceItem.durationInHours}"

def testInvoiceItemToJSON():
    invoiceItemJson = objectToJson(invoiceItem)
    expectedJson = '{"id": "0001", "projectId": "0001", "description": "A test item", "billable": false, "startTimeEpochInSeconds": 1662836400, "endTimeEpochInSeconds": 1662838200, "durationInSeconds": 1800}'
    assert invoiceItemJson == expectedJson, f"""Expecting:
{expectedJson}
Got:
{invoiceItemJson}
"""

if __name__ == "__main__":
    testInvoiceItemDuration()
    testInvoiceItemToJSON()
    print("Done test_models")