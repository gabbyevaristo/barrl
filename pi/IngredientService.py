import json
import os
import uuid
import pi.jsonService as jsonService

if os.environ['ENV'] == "dev":
    import pi.MockGpio as GPIO
else:
    import RPi.GPIO as GPIO

defaultIngredientfilePath = "./jsonFiles/ingredients.json"
defaultPumpMapfilePath = "./jsonFiles/pumpMap.json"

# in ml per second
pumpRate = {
    0: 80.0/60.0, 
    1: 80.0/60.0,
    2: 80.0/60.0,
    3: 80.0/60.0,
    4: 80.0/60.0,
    5: 80.0/60.0
}

def convertBottlesToIngredients(bottlesFilePath="./bottles.json"):
    bottles = jsonService.loadJson(bottlesFilePath)

    pumpNumber = 0
    for bottleNum in bottles:
        bottle = bottles[bottleNum]
        addIngredient(name=bottle["name"], pumpNumber=pumpNumber, size=bottle["size"], ml=bottle["ml"], brand=bottle["brand"] , drinkType=bottle["type"] , estimated_fill=bottle["estimated_fill"], image=bottle["image"])
        if pumpNumber >= 0 and pumpNumber < 6:
            pumpNumber += 1
        if pumpNumber >= 6:
            pumpNumber = -1


def clearIngredients(ingredientfilePath=defaultIngredientfilePath):
    jsonService.saveJson({}, ingredientfilePath)

def isValidPumpNumber(pumpNumber):
    return pumpNumber >= 0 and pumpNumber < 6 

def clearPumpMap(pumpMapfilePath=defaultPumpMapfilePath):
    pumpMap = {}
    for i in range(6):
        pumpMap[str(i)] = None
    jsonService.saveJson(pumpMap, pumpMapfilePath)

def modifyPumpMapp(ingGuid, pumpNumber, pumpMapfilePath=defaultPumpMapfilePath):
    pumpMap = jsonService.loadJson(pumpMapfilePath)
    if not isValidPumpNumber(pumpNumber):
        print("Pump number out of range when updating pump map")
        return
    
    # remove old entries if they exist so we can maintain two way dictionary
    oldLiquid = pumpMap[str(pumpNumber)]
    if oldLiquid is not None:
        del pumpMap[oldLiquid]

    del pumpMap[str(pumpNumber)]

    # pumpMap[str(pumpNumber)] = ingGuid
    pumpMap[str(pumpNumber)] = ingGuid
    pumpMap[ingGuid] = pumpNumber
    jsonService.saveJson(pumpMap, pumpMapfilePath)

def getPumpMap(pumpMapfilePath=defaultPumpMapfilePath):
    pumpMap = jsonService.loadJson(pumpMapfilePath)

    # json does not support integer keys 
    # we store keys as strings but we convert them to also have integers for ease of use
    i = 0
    while isValidPumpNumber(i):
        if str(i) in pumpMap:
            pumpMap[i] = pumpMap[str(i)]
        i += 1

    return pumpMap
        
# add all these atributes to ingredient and assign it a guid
# additional attributes can be addded through kwargs
def addIngredient(name="", pumpNumber=-1, size= "1L", ml=1000, brand= "", drinkType= "", estimated_fill= "", image= "", ingredientfilePath=defaultIngredientfilePath, **kwargs):
    ing = { 
            "name": name \
            ,"size": size \
            ,"ml": ml \
            ,"brand": brand \
            ,"type": drinkType \
            ,"estimated_fill": estimated_fill \
            ,"image": image \
            # ,"pumpNumber": pumpNumber \
          }

    for key, value in kwargs.items():
        ing[key] = value

    guid = str(uuid.uuid1())

    if isValidPumpNumber(pumpNumber):
        modifyPumpMapp(guid, pumpNumber)

    allIngs = jsonService.loadJson(ingredientfilePath)
    if guid in allIngs:
        print("Collision in ID when adding ingredient")
    allIngs[guid] = ing
    jsonService.saveJson(allIngs, ingredientfilePath) 

    print("Added Ingredient")
    print(guid)
    print(ing)

def modifyIngredient(guid, name="", pumpNumber=-1, size= "1L", ml=1000, brand= "", drinkType= "", estimated_fill= "", image= "", ingredientfilePath=defaultIngredientfilePath, **kwargs):
    ing = { 
            "name": name \
            ,"size": size \
            ,"ml": ml \
            ,"brand": brand \
            ,"type": drinkType \
            ,"estimated_fill": estimated_fill \
            ,"image": image \
            # ,"pumpNumber": pumpNumber \
          }

    for key, value in kwargs.items():
        ing[key] = value

    allIngs = jsonService.loadJson(ingredientfilePath)
    if guid not in allIngs:
        print("Attempted to modify ingredient that is not in database")
        return 

    allIngs[guid] = ing

    if isValidPumpNumber(pumpNumber):
        modifyPumpMapp(guid, pumpNumber)

    jsonService.saveJson(allIngs, ingredientfilePath) 

    print("Modified Ingredient")
    print(guid)
    print(ing)

def removeIngredientByGuid(guid, ingredientfilePath=defaultIngredientfilePath):
    allIngs = jsonService.loadJson(ingredientfilePath)
    if guid in allIngs:
        del allIngs[guid]
    jsonService.saveJson(allIngs, ingredientfilePath) 

def getIngredientByGuid(guid, ingredientfilePath=defaultIngredientfilePath):
    allIngs = jsonService.loadJson(ingredientfilePath)

    if guid in allIngs:
        ret = allIngs[guid]
    else:
        print("Guid %s not in ingredients" % guid)
        return None
    
    return ret

def getAllIngredients(ingredientfilePath=defaultIngredientfilePath):
    allIngs = jsonService.loadJson(ingredientfilePath)
    return allIngs

# if ingredients are not present, then create file so everything does not break
if not os.path.exists(defaultIngredientfilePath):
    clearIngredients()

if not os.path.exists(defaultPumpMapfilePath):
    clearPumpMap()
    