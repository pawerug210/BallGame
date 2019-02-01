from collections import namedtuple
import json

def getParams(filename):
    with open(filename) as f:
        data = json.load(f)
    return namedtuple("params", data.keys())(*data.values())