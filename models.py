class Project:
    def __init__(
        self,
        id,
        name,
        billable,
        hourlyRate,
        clientId
    ) -> None:
        self.id = str(id)
        self.name = name
        self.billable = billable or True
        self.hourlyRate = hourlyRate or 0.0
        self.clientId = str(clientId)


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
        self.id = str(id)
        self.projectId = str(projectId)
        self.description = description
        self.billable = billable
        self.startTimeEpochInSeconds = startTimeEpochInSeconds
        self.endTimeEpochInSeconds = endTimeEpochInSeconds
        self.durationInSeconds = durationInSeconds


class Company:
    def __init__(
        self,
        clientId:str,
        clientName:str,
        address:str,
        cityCountryZipcode:str,
        phoneNumber:str,
        projectName:str,
        projectDescription:str,
    ):
        self.clientId = str(clientId)
        self.clientName = clientName
        self.address = address
        self.cityCountryZipcode = cityCountryZipcode
        self.phoneNumber = phoneNumber
        self.projectName = projectName
        self.projectDescription = projectDescription


# Meta-data for the header of the invoice
class InvoiceHeaderData:
    def __init__(
        self,
        invoicePreparedOnDate:str,
        invoiceNumber:str,
        invoiceStartDate:str,
        invoiceEndDate:str,
        fromCompany:Company,
        toCompany:Company
    ):
        self.invoicePreparedOnDate = invoicePreparedOnDate
        self.invoiceNumber = invoiceNumber
        self.invoiceStartDate = invoiceStartDate
        self.invoiceEndDate = invoiceEndDate

        self.fromCompany = fromCompany
        self.toCompany = toCompany
