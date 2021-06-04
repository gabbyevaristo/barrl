
from os import waitpid
import pi.IngredientService as IngredientService
import pi.MenuService as MenuService
import pi.PouringService as PouringService


IngredientService.clearPumpMap()
IngredientService.clearIngredients()
vodka = IngredientService.addIngredient(name="Vodka", pumpNumber=0, ml=1750, brand="Titos", type="alchool", estimated_fill="100", image=None)
tequila = IngredientService.addIngredient(name="Tequila", pumpNumber=1, ml=1750, brand="Patron", type="alchool", estimated_fill="100", image=None)
spirte = IngredientService.addIngredient(name="Sprite", pumpNumber=2, ml=2000, brand="Sprite", type="mixer", estimated_fill="100", image=None)
clubSoda = IngredientService.addIngredient(name="Club Soda", pumpNumber=3, ml=2000, brand="Canada Dry", type="mixer", estimated_fill="100", image=None)
orangeJuice = IngredientService.addIngredient(name="Orange Juice", pumpNumber=4, ml=3785, brand="Minute Made", type="mixer", estimated_fill="100", image=None)
limeJuice = IngredientService.addIngredient(name="Lime Juice", pumpNumber=5, ml=1000, brand="Real Lime", type="mixer", estimated_fill="100", image=None)

MenuService.clearMenu()
MenuService.addDrinkToMenu("Vodka Shot", {vodka: 50}, price=4.99, image=None, description="A standard shot of vodka", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Tequila Shot", {tequila: 50}, price=4.99, image=None, description="A standard shot of tequila", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Vodka Soda", {vodka: 50, clubSoda: 150}, price=6.99, image=None, description="Vodka mixed with club soda", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Screwdriver", {vodka: 50, orangeJuice: 150}, price=6.99, image=None, description="Vodka mixed with orange juice", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Vodka and Lime", {vodka: 50, limeJuice: 100}, price=6.99, image=None, description="Vodka mixed with lime juice", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Vodka and Sprite", {vodka: 50, spirte: 150}, price=6.99, image=None, description="Vodka mixed with Sprite", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Tequila and Sprite", {tequila: 50, spirte: 150}, price=6.99, image=None, description="Tequila mixed with Sprite", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Tequila Soda", {tequila: 50, clubSoda: 150}, price=6.99, image=None, description="Tequila mixed with club soda", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Tequila Sunrise", {tequila: 50, orangeJuice: 150}, price=7.99, image=None, description="Tequila mixed with orange juice", menuFilePath=MenuService.defaultMenufilePath)
MenuService.addDrinkToMenu("Tequila and Lime", {tequila: 50, limeJuice: 100}, price=6.99, image=None, description="Tequila mixed with lime juice", menuFilePath=MenuService.defaultMenufilePath)
