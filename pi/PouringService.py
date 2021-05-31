import os 
if os.environ['ENV'] == "dev":
    import pi.MockGpio as GPIO
else:
    import RPi.GPIO as GPIO

import time
import pi.IngredientService as IngredientService
import pi.MenuService as MenuService


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


def pourDrink(drinkGuid, menuFilePath=MenuService.defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
    if not MenuService.isValidDrinkToPour(drinkGuid, menuFilePath=menuFilePath, ingredientfilePath=ingredientfilePath, pumMapfilePath=pumMapfilePath):
        print("Skipping drink to pour due to invalid drink enty")
        return

    menu = MenuService.getMenu()
    drink = menu[drinkGuid]
    pumpMap = IngredientService.getPumpMap()

    for ing, amount in drink["ings"].items():
        pumpNum = pumpMap[ing]
        pourFromPump(pumpNum, amount)
