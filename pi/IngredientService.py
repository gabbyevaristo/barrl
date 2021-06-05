import pi.jsonService as jsonService
import json
import uuid
import os


defaultIngredientfilePath = './jsonFiles/ingredients.json'
defaultPumpMapfilePath = './jsonFiles/pumpMap.json'


# Pump rate in mL per second
pumpRate = {
    0: 80.0/60.0,
    1: 80.0/60.0,
    2: 80.0/60.0,
    3: 80.0/60.0,
    4: 80.0/60.0,
    5: 80.0/60.0
}


''' Script to convert from old bottles format to new format '''
def convertBottlesToIngredients(bottlesFilePath='./bottles.json'):
    bottles = jsonService.loadJson(bottlesFilePath)
    pumpNumber = 0
    for bottleNum in bottles:
        bottle = bottles[bottleNum]
        addIngredient(name=bottle['name'], pumpNumber=pumpNumber, ml=bottle['ml'], brand=bottle['brand'], drinkType=bottle['type'], estimatedFill=bottle['estimated_fill'], image=bottle['image'])
        if pumpNumber >= 0 and pumpNumber < 6:
            pumpNumber += 1
        if pumpNumber >= 6:
            pumpNumber = -1


def clearPumpMap(pumpMapfilePath=defaultPumpMapfilePath):
    pumpMap = {}
    for i in range(6):
        pumpMap[str(i)] = None
    jsonService.saveJson(pumpMap, pumpMapfilePath)


def isValidPumpNumber(pumpNumber):
    return pumpNumber >= 0 and pumpNumber < 6


def modifyPumpMap(ingGuid, pumpNumber, pumpMapfilePath=defaultPumpMapfilePath):
    if not isValidPumpNumber(pumpNumber):
        print('Pump number out of range when updating pump map')
        return

    pumpMap = jsonService.loadJson(pumpMapfilePath)

    # Remove old entries if they exist so we can maintain a two-way dictionary
    oldIng = pumpMap.get(str(pumpNumber))
    if oldIng is not None:
        del pumpMap[oldIng]
    pumpMap.pop(str(pumpNumber), None)

    # Save pump to ingredient and ingredient to pump mapping
    pumpMap[ingGuid] = pumpNumber
    pumpMap[str(pumpNumber)] = ingGuid

    jsonService.saveJson(pumpMap, pumpMapfilePath)


def getPumpMap(pumpMapfilePath=defaultPumpMapfilePath):
    pumpMap = jsonService.loadJson(pumpMapfilePath)

    # json does not support integer keys. Keys are stored as strings, but we
    # convert them to also use integers for ease of use
    i = 0
    while isValidPumpNumber(i):
        if str(i) in pumpMap:
            pumpMap[i] = pumpMap[str(i)]
        i += 1

    return pumpMap


def clearIngredients(ingredientfilePath=defaultIngredientfilePath):
    jsonService.saveJson({}, ingredientfilePath)


# Add ingredient with the specified attributes and assign it to a guid
'''
Additional attributes can be addded through kwargs
'''
def addIngredient(name='', pumpNumber=-1, ml=1000, brand='', drinkType='', estimatedFill='', image='', ingredientfilePath=defaultIngredientfilePath, **kwargs):
    ing = {
            'name': name, \
            'ml': ml, \
            'brand': brand, \
            'type': drinkType, \
            'estimated_fill': estimatedFill, \
            'image': image
          }

    for key, value in kwargs.items():
        ing[key] = value

    guid = str(uuid.uuid1())

    allIngs = jsonService.loadJson(ingredientfilePath)
    if guid in allIngs:
        print('Collision in ID when adding ingredient')
    allIngs[guid] = ing
    jsonService.saveJson(allIngs, ingredientfilePath)

    if isValidPumpNumber(pumpNumber):
        modifyPumpMap(guid, pumpNumber)

    return guid


def modifyIngredient(guid, name='', pumpNumber=-1, ml=1000, brand='', drinkType='', estimatedFill='', image= '', ingredientfilePath=defaultIngredientfilePath, **kwargs):
    ing = {
            'name': name, \
            'ml': ml, \
            'brand': brand, \
            'type': drinkType, \
            'estimated_fill': estimatedFill, \
            'image': image
          }

    for key, value in kwargs.items():
        ing[key] = value

    allIngs = jsonService.loadJson(ingredientfilePath)
    if guid not in allIngs:
        print('Attempted to modify ingredient not in database')
        return

    allIngs[guid] = ing
    jsonService.saveJson(allIngs, ingredientfilePath)

    if isValidPumpNumber(pumpNumber):
        modifyPumpMap(guid, pumpNumber)


def removeIngredientByGuid(guid, ingredientfilePath=defaultIngredientfilePath, pumpMapfilePath=defaultPumpMapfilePath):
    allIngs = jsonService.loadJson(ingredientfilePath)
    pumpMap = jsonService.loadJson(pumpMapfilePath)
    pumpNum = pumpMap.get(guid)

    # Remove mappings from pump map if guid was connected to a pump
    if pumpNum != None:
        del pumpMap[str(pumpNum)]
        del pumpMap[guid]

    if guid in allIngs:
        del allIngs[guid]

    jsonService.saveJson(pumpMap, pumpMapfilePath)
    jsonService.saveJson(allIngs, ingredientfilePath)


def getIngredientByGuid(guid, ingredientfilePath=defaultIngredientfilePath):
    allIngs = jsonService.loadJson(ingredientfilePath)
    if guid in allIngs:
        ret = allIngs[guid]
    else:
        print('Guid %s not in ingredients' % guid)
        return None
    return ret


def getAllIngredients(ingredientfilePath=defaultIngredientfilePath):
    allIngs = jsonService.loadJson(ingredientfilePath)
    return allIngs


# If ingredients file does not exist, then create it so everything does not break
if not os.path.exists(defaultIngredientfilePath):
    clearIngredients()


# If pump map file does not exist, then create it so everything does not break
if not os.path.exists(defaultPumpMapfilePath):
    clearPumpMap()
