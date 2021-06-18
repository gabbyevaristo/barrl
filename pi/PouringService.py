import pi.IngredientService as IngredientService
import pi.MenuService as MenuService
import time
import os


import pi.MockGpio as GPIO
# if os.environ['ENV'] == 'dev':
#     import pi.MockGpio as GPIO
# else:
#     import RPi.GPIO as GPIO


# Get mapping of pump numbers to pins
pumpToPin = {
    0: 36,
    1: 22,
    2: 18,
    3: 11,
    4: 13,
    5: 15
}

# Get mapping of pins to pump numbers
pinToPump = {}
for pump, pin in pumpToPin.items():
    pinToPump[pin] = pump

# Initialize pins on board
GPIO.setmode(GPIO.BOARD)
for pin in pinToPump:
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)


# Pour liquid from specified pump number, where amount is in mL
def pourFromPump(pumpNumber, amount):
    global pumpToPin
    if pumpNumber not in pumpToPin:
        print('Tried to pour a liquid from a pump that is not in the pin map')
        return

    pinNumber = pumpToPin[pumpNumber]
    duration = amount / IngredientService.pumpRate[pumpNumber]
    print('Pin ON %d' % pinNumber)
    GPIO.output(pinNumber, False)
    time.sleep(duration)
    GPIO.output(pinNumber, True)
    print('Pin OFF %d' % pinNumber)


# Pour drink given by drinkGuid
def pourDrink(drinkGuid, menuFilePath=MenuService.defaultMenufilePath, ingredientfilePath=IngredientService.defaultIngredientfilePath, pumMapfilePath=IngredientService.defaultPumpMapfilePath):
    if not MenuService.isValidDrinkToPour(drinkGuid, menuFilePath=menuFilePath, ingredientfilePath=ingredientfilePath, pumMapfilePath=pumMapfilePath):
        print('Skipping drink to pour due to invalid drink entry')
        return

    menu = MenuService.getMenu()
    drink = menu[drinkGuid]
    pumpMap = IngredientService.getPumpMap()

    for ing, amount in drink['ings'].items():
        pumpNum = pumpMap[ing]
        pourFromPump(pumpNum, amount)


'''
Make sure user attaches water to the pumps before pumps are turned on. If pumpNumber
is None, then all pumps are cleaned, else only the specified pump is cleaned.
'''
def cleanPump(pumpNumber=None, amount=100):
    if pumpNumber is not None:
        if IngredientService.isValidPumpNumber(pumpNumber):
            pourFromPump(pumpNumber, amount)
        else:
            print('Attempted to clean invalid pump number')
    else:
        for pump in pumpToPin:
            pourFromPump(pump, amount)
