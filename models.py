class Project:
    def __init__(
        self,
        name:str,
        ratePerHour:float
    ):
        self.name = name
        self.ratePerHour = ratePerHour


class InvoiceItem:
    def __init__(
        self,
        id:str,
        project:Project,
        title:str,
        description:str,
        startTimeEpochInSeconds:int,
        endTimeEpochInSeconds:int
    ):
        self.id = id
        self.project = project
        self.title = title
        self.description = description
        self.startTimeEpochInSeconds = startTimeEpochInSeconds
        self.endTimeEpochInSeconds = endTimeEpochInSeconds

    @property
    def durationInHours(self):
        return (self.endTimeEpochInSeconds - self.startTimeEpochInSeconds) / 3.6e3


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
