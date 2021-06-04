import time
import pi.IngredientService as IngredientService
import pi.MenuService as MenuService
# from joblib import Parallel, delayed

import os 
# if os.environ['ENV'] == "dev":
#     import pi.MockGpio as GPIO
# else:
#     import RPi.GPIO as GPIO

import RPi.GPIO as GPIO


# get mapping of pump numbers to pins
pumpToPin = {
    0: 36, 
    1: 22, 
    2: 18,
    3: 11,
    4: 13,
    5: 15
}

# get the reverse mapping
pinToPump = {}
for pump,pin in pumpToPin.items():
    pinToPump[pin] = pump

# initialize pins on board
GPIO.setmode(GPIO.BOARD)
for pin in pinToPump:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)


# amount in ml
def pourFromPump(pumpNumber, amount):
    global pumpToPin
    if pumpNumber not in pumpToPin:
        print("Tried to pour a liquid from a pump that is not in the pin map")
        print(pumpNumber)
        print(type(pumpNumber))
        return

    pinNumber = pumpToPin[pumpNumber]
    duration = amount / IngredientService.pumpRate[pumpNumber]
    print("Pin ON %d" % pinNumber)
    GPIO.output(pinNumber,False)
    time.sleep(duration)
    GPIO.output(pinNumber,True)
    print("Pin OFF %d" % pinNumber)


# if n_jobs is -1 then standard serial pumping loop is excecuted
def pourDrink(drinkGuid, menuFilePath=MenuService.defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
# def pourDrink(drinkGuid, menuFilePath=MenuService.defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath, n_jobs=6):
    if not MenuService.isValidDrinkToPour(drinkGuid, menuFilePath=menuFilePath, ingredientfilePath=ingredientfilePath, pumMapfilePath=pumMapfilePath):
        print("Skipping drink to pour due to invalid drink enty")
        return

    menu = MenuService.getMenu()
    drink = menu[drinkGuid]
    pumpMap = IngredientService.getPumpMap()

    for ing, amount in drink["ings"].items():
        pumpNum = pumpMap[ing]
        pourFromPump(pumpNum, amount)

    # if n_jobs == -1:
    #     for ing, amount in drink["ings"].items():
    #         pumpNum = pumpMap[ing]
    #         pourFromPump(pumpNum, amount)
    # else:
    #     Parallel(n_jobs=n_jobs)(delayed(pourFromPump)(pumpMap[ing], amount) for ing, amount in drink["ings"].items())



# be sure user attaches water to the pumps before pumps are turned on
# if pumpNumber is None, then all pumps are cleaned else only specified pump 
def cleanPump(pumpNumber=None, amount=100):
    if pumpNumber is not None:
        if IngredientService.isValidPumpNumber(pumpNumber):
            pourFromPump(pumpNumber, amount)
        else:
            print("Attempted to clean invalid pump number")
    else:
        for pump in pumpToPin:
            pourFromPump(pump, amount)
    
