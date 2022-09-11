import utilities
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from base64 import b64encode


# References https://developers.track.toggl.com/docs/authentication/index.html#http-basic-auth-with-api-token
def generateRequestHeader(apiToken:str):
    return {'content-type': 'application/json', 'Authorization' : 'Basic %s' %  b64encode(f"{apiToken}:api_token".encode("ascii")).decode("ascii")}

def _makeRequestReturnJsonDict(url:str, requestHeader:dict):
    req = Request(url)
    for header in requestHeader:
        req.add_header(header, requestHeader[header])
    try:
        data = urlopen(req).read()
        data = utilities.jsonToDict(data)
    except URLError as e:
        print(e.reason)
        if isinstance(e, HTTPError):
            print(e.read().decode())
        raise e
        
    return data


def getAllProjects(apiEndpoint:str, requestHeader:dict):
    return _makeRequestReturnJsonDict(f"{apiEndpoint}/me/projects", requestHeader=requestHeader)
    
def getAllTimeEntries(apiEndpoint:str,startDateEpoch:int,endDateEpoch:int, requestHeader:dict):
    startDate = utilities.epochToYYYY_MM_DDString(startDateEpoch)
    endDate = utilities.epochToYYYY_MM_DDString(endDateEpoch)
    return _makeRequestReturnJsonDict(
        f"{apiEndpoint}/me/time_entries?start_date={startDate}&end_date={endDate}",
        requestHeader=requestHeader
    )