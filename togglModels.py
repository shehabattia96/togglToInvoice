import models
from utilities import isoDateStringToEpochSeconds

def mapTogglePayloadToProject(
        id,
        name,
        billable,
        rate,
        client_id,
        fixed_fee,
        **payloadFromToggl
    ):
        return models.Project(
            id=id,
            name=name,
            billable=billable or True,
            hourlyRate=rate or 0.0,
            clientId=client_id,
        )
def mapTogglePayloadToInvoiceItem(
        id,
        description,
        start, #start date in iso format
        stop, #end date in iso format
        duration,
        project_id,
        billable,
        tag_ids,
        tags,
        **payloadFromToggl
    ) -> None:
        return models.InvoiceItem(
            id=id,
            projectId=project_id,
            description=description,
            billable=billable or False,
            startTimeEpochInSeconds=isoDateStringToEpochSeconds(start),
            endTimeEpochInSeconds=isoDateStringToEpochSeconds(stop),
            durationInSeconds=duration
        )