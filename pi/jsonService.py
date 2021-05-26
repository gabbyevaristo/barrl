import json

def loadJson(filePath):
    ret = None
    with open(filePath, "r") as file:
        ret = json.load(file)
    return ret


def saveJson(obj, filePath):
    with open(filePath, "w") as file:
        json.dump(obj, file, indent=4, sort_keys=True)
