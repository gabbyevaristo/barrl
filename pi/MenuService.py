import pi.IngredientService as IngredientService
import pi.jsonService as jsonService
import uuid
import os
import random


defaultMenufilePath = './jsonFiles/menu.json'


def clearMenu(menuFilePath=defaultMenufilePath):
    jsonService.saveJson({}, menuFilePath)


randDrinkNumber = 0
def generateRandomDrink(maxIngredient=4, maxMl=100):
    global randDrinkNumber
    drink = {}
    drink['name'] = 'Random Drink %d' % randDrinkNumber
    randDrinkNumber += 1
    drink['description'] = ''
    drink['price'] = round(random.random() * 10, 2)
    drink['image'] = 'https://static5.depositphotos.com/1008347/501/i/600/depositphotos_5019783-stock-photo-cocktail-splashing.jpg'

    # Generate random ingredient-amount pairs
    numIngs = random.randrange(maxIngredient) + 1
    allIngs = IngredientService.getAllIngredients()
    ings = {}
    for i in range(numIngs):
        allKeys = list(allIngs.keys())
        key = random.choice(allKeys)
        del allIngs[key]
        amount = float(random.randrange(maxMl))
        ings[key] = amount
    drink['ings'] = ings

    return drink


''' ings = dictionary with {'ing guid': mL of ing} '''
def addDrinkToMenu(name, ings, description='', price=0.0, image='', menuFilePath=defaultMenufilePath):
    drink = {}
    drink['name'] = name
    drink['description'] = description
    drink['price'] = price
    drink['image'] = image
    drink['ings'] = {}

    allIngs = IngredientService.getAllIngredients()
    for ing in ings:
        if ing in allIngs:
            drink['ings'][ing] = float(ings[ing])
        else:
            print('When adding drink, %s not in ingredient database. Skipping ingredient' % ing)

    guid = str(uuid.uuid1())

    menu = jsonService.loadJson(menuFilePath)
    if guid in menu:
        print('Collision in guid when adding drink to menu')
    menu[guid] = drink
    jsonService.saveJson(menu, menuFilePath)

    return guid


def modifyDrink(guid, name, ings, description='', price=0.0, image='', menuFilePath=defaultMenufilePath):
    drink = {}
    drink['name'] = name
    drink['description'] = description
    drink['price'] = price
    drink['image'] = image
    drink['ings'] = {}

    allIngs = IngredientService.getAllIngredients()
    for ing in ings:
        if ing in allIngs:
            drink['ings'][ing] = float(ings[ing])
        else:
            print('When adding drink, %s not in ingredient database. Skipping ingredient' % ing)

    menu = jsonService.loadJson(menuFilePath)
    if guid not in menu:
        print('Attempted to modify drink not in menu')
        return

    menu[guid] = drink
    jsonService.saveJson(menu, menuFilePath)


def removeDrinkByGuid(guid, menuFilePath=defaultMenufilePath):
    menu = jsonService.loadJson(menuFilePath)
    if guid in menu:
        del menu[guid]
    jsonService.saveJson(menu, menuFilePath)


def getDrinkByGuid(guid, menuFilePath=defaultMenufilePath):
    menu = jsonService.loadJson(menuFilePath)
    if guid in menu:
        ret = menu[guid]
    else:
        print('Guid %s not in menu' % guid)
        return None
    return ret


def getMenu(menuFilePath=defaultMenufilePath):
    menu = jsonService.loadJson(menuFilePath)
    return menu


def isValidDrinkInDb(drinkGuid, menuFilePath=defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
    menu = getMenu(menuFilePath)
    if drinkGuid not in menu:
        print('Drink %s not in menu' % drinkGuid)
        return False

    allIngs = IngredientService.getAllIngredients(ingredientfilePath)
    pumpMap = IngredientService.getPumpMap(pumMapfilePath)
    drink = menu[drinkGuid]
    for ingGuid in drink['ings']:
        if ingGuid not in allIngs:
            print('Drink ingredient %s not in ingredient database' % ingGuid)
            return False

    return True


def isValidDrinkToPour(drinkGuid, menuFilePath=defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
    menu = getMenu(menuFilePath)
    if drinkGuid not in menu:
        print('Drink %s not in menu' % drinkGuid)
        return False

    allIngs = IngredientService.getAllIngredients(ingredientfilePath)
    pumpMap = IngredientService.getPumpMap(pumMapfilePath)
    drink = menu[drinkGuid]
    for ingGuid in drink['ings']:
        if ingGuid not in allIngs:
            print('Drink ingredient %s not in ingredient database' % ingGuid)
            return False
        if ingGuid not in pumpMap:
            print('Drink ingredient %s not on tap' % ingGuid)
            return False

    return True


# If menu file does not exist, then create it so everything does not break
if not os.path.exists(defaultMenufilePath):
    clearMenu()
