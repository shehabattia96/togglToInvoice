class Project:
    def __init__(
        self,
        id,
        name,
        billable,
        hourlyRate,
        clientId
    ) -> None:
        self.id = id
        self.name = name
        self.billable = billable or True
        self.hourlyRate = hourlyRate or 0.0
        self.clientId = clientId


class InvoiceItem:
    def __init__(
        self,
        id:str,
        projectId:str,
        description:str,
        billable:bool,
        startTimeEpochInSeconds:int,
        endTimeEpochInSeconds:int,
        durationInSeconds:int
    ):
        self.id = id
        self.projectId = projectId
        self.description = description
        self.billable = billable
        self.startTimeEpochInSeconds = startTimeEpochInSeconds
        self.endTimeEpochInSeconds = endTimeEpochInSeconds
        self.durationInSeconds = durationInSeconds


class Company:
    def __init__(
        self,
        name:str,
        address:str,
        cityCountryZipcode:str,
        phoneNumber:str
    ):
        self.name = name
        self.address = address
        self.cityCountryZipcode = cityCountryZipcode
        self.phoneNumber = phoneNumber


# Meta-data for the header of the invoice
class InvoiceHeaderData:
    def __init__(
        self,
        invoicePreparedOnDate:str,
        invoiceNumber:str,
        invoiceStartDate:str,
        invoiceEndDate:str,
        projectName:str,
        projectDescription:str,
        fromCompany:Company,
        toCompany:Company
    ):
        self.invoicePreparedOnDate = invoicePreparedOnDate
        self.invoiceNumber = invoiceNumber
        self.invoiceStartDate = invoiceStartDate
        self.invoiceEndDate = invoiceEndDate

        self.projectName = projectName
        self.projectDescription = projectDescription

        self.fromCompany = fromCompany
        self.toCompany = toCompany
