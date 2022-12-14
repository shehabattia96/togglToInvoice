import json
from datetime import datetime, timedelta

def isoDateStringToEpochSeconds(isoDateString):
    # references https://stackoverflow.com/a/59744630
    if isoDateString[-1].lower() == "z":
        isoDateString = isoDateString[:-1] + '+00:00'
    return datetime.fromisoformat(isoDateString).timestamp()
def epochToIsoDateString(epochInSeconds):
    return datetime.fromtimestamp(epochInSeconds).isoformat()
def epochToMMDDYYYYString(epochInSeconds):
    return datetime.fromtimestamp(epochInSeconds).strftime("%m/%d/%Y")
def epochToBDDYYYYString(epochInSeconds):
    return datetime.fromtimestamp(epochInSeconds).strftime("%b %d %Y")
def epochToYYYY_MM_DDString(epochInSeconds):
    return datetime.fromtimestamp(epochInSeconds).strftime("%Y-%m-%d")
def epochNowInSeconds():
    return int(datetime.now().timestamp())
def secondsToHours(seconds):
    return round(seconds/3.6e3,2)
def secondsToHoursMinutesSeconds(seconds):
    return format_timedelta(timedelta(seconds=seconds))

# references https://stackoverflow.com/a/28503916/9824103
def format_timedelta(td:timedelta):
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

# tech debt: this will only work for a single layer of obj nesting.
class NestedObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            return obj.__dict__

def objectToJson(object, prettify=False):
    return json.dumps(object, indent= 4 if prettify else None, cls=NestedObjectEncoder)

def jsonToDict(jsonString:str):
    return json.loads(jsonString)

def readJsonFromFile(filePath:str):
    fileHandler = open(filePath)
    data = json.load(fileHandler)
    fileHandler.close()
    return data


def writeToFile(fileName, data):
    fileHandler = open(fileName, "w")
    fileHandler.write(data)
    fileHandler.close()