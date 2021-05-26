import os
import uuid
import pi.IngredientService as IngredientService
import pi.jsonService as jsonService
import random

defaultMenufilePath = "./jsonFiles/menu.json"


def clearMenu(menuFilePath=defaultMenufilePath):
    jsonService.saveJson({}, menuFilePath)
        

randDrinkNumber = 0
def generateRandomDrink(maxIngredient=4, maxMl=100):
    global randDrinkNumber
    drink = {}
    drink["name"] = "Random Drink %d" % randDrinkNumber
    randDrinkNumber += 1
    drink["price"] = random.random() * 10
    drink["image"] = ""

    numIngs = random.randrange(maxIngredient) + 1
    allIngs = IngredientService.getAllIngredients()
    ings = {}
    for i in range(0, numIngs):
        allKeys =  list(allIngs.keys())
        key = random.choice(allKeys)
        del allIngs[key]
        amount = float(random.randrange(maxMl))
        ings[key] = amount
    drink["ings"] = ings

    return drink
   


# ings - dictionary with {"ing guid":ml of ing}
def addDrinkToMenu(name, ings, price=0.0, image="", menuFilePath=defaultMenufilePath):

    allIngs = IngredientService.getAllIngredients()
    drink = {}
    drink["name"] = name
    drink["price"] = price
    drink["image"] = image
    drink["ings"] = {}
    
    for ing in ings:
        if ing in allIngs:
            drink["ings"][ing] = float(ings[ing])
        else:
            print("when adding drink ingredient not in ingredient database, skipping ingredient")
            print(ing)

    guid = str(uuid.uuid1())

    menu = jsonService.loadJson(menuFilePath)
    if guid in menu:
        print("collision in guid when adding drink to menu")
    menu[guid] = drink
    jsonService.saveJson(menu, menuFilePath)

    print("Added drink to menu")
    print(drink)
    print(guid)

def removeDrinkByGuid(guid, menuFilePath=defaultMenufilePath):
    menu = jsonService.loadJson(menuFilePath)
    if guid in menu:
        del menu[guid]
    jsonService.saveJson(menu, menuFilePath)

def getDrinkByGuid(guid):
    menu = jsonService.loadJson(menuFilePath)
    if guid in menu:
        ret = menu[guid]
    else:
        print("Guid %s not in ingredients" % guid)
        return None
    return ret

def getMenu(menuFilePath=defaultMenufilePath):
    menu = jsonService.loadJson(menuFilePath)
    return menu

def isValidDrinkInDb(drinkGuid, menuFilePath=defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
    menu = getMenu(menuFilePath)
    if drinkGuid not in menu:
        print("Drink not in menu")
        print(drinkGuid)
        return False
    allIngs = IngredientService.getAllIngredients(ingredientfilePath)
    pumpMap = IngredientService.getPumpMap(pumMapfilePath)
    drink = menu[drinkGuid]
    for ingGuid in drink["ings"]:
        if ingGuid not in allIngs:
            print("Drink ingredient not in ingredient database")
            print(ingGuid)
            return False
        # this function just checks if drink is makeable from database, not pourable
        # if ingGuid not in pumpMap:
            # print("Drink ingredient not on tap")
            # print(ingGuid)
            # return False

    return True

def isValidDrinkToPour(drinkGuid, menuFilePath=defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
    menu = getMenu(menuFilePath)
    if drinkGuid not in menu:
        print("Drink not in menu")
        print(drinkGuid)
        return False
    allIngs = IngredientService.getAllIngredients(ingredientfilePath)
    pumpMap = IngredientService.getPumpMap(pumMapfilePath)
    drink = menu[drinkGuid]
    for ingGuid in drink["ings"]:
        if ingGuid not in allIngs:
            print("Drink ingredient not in ingredient database")
            print(ingGuid)
            return False
        if ingGuid not in pumpMap:
            print("Drink ingredient not on tap")
            print(ingGuid)
            return False

    return True

    

# if ingredients are not present, then creat file so everything doesnt break
if not os.path.exists(defaultMenufilePath):
    clearMenu()
