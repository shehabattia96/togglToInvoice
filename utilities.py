import json
from datetime import datetime

def isoDateStringToEpoch(isoDateString):
    return datetime.fromisoformat(isoDateString).timestamp()
def epochToIsoDateString(epoch):
    return datetime.fromtimestamp(epoch).isoformat()
def epochToMMDDYYYYString(epoch):
    return datetime.fromtimestamp(epoch).strftime("%m/%d/%Y")


# tech debt: this will only work for a single layer of obj nesting.
class NestedObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            return obj.__dict__


def objectToJson(object):
    return json.dumps(object, cls=NestedObjectEncoder)

def jsonToDict(jsonString:str):
    return json.loads(jsonString)