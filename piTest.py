from os import waitpid
import pi.IngredientService as IngredientService
import pi.MenuService as MenuService
import pi.PouringService as PouringService


# IngredientService.clearPumpMap()
# IngredientService.addIngredient(name="Vodka", ml=1000, brand="Titos", type="alcohol", estimated_fill="50", image="here")
# IngredientService.clearIngredients()
# IngredientService.convertBottlesToIngredients()

# MenuService.clearMenu()
# for i in range(8):
    # drink = MenuService.generateRandomDrink()
    # MenuService.addDrinkToMenu(**drink)

# print("---------------------------------------")
# print(MenuService.isValidDrinkInDb("a"))
# print("---------------------------------------")
# print(MenuService.isValidDrinkInDb("3f58dd75-bb21-11eb-8145-b831b5854dfb"))
# print("---------------------------------------")
# print(MenuService.isValidDrinkInDb("3f59519c-bb21-11eb-960c-b831b5854dfb"))

PouringService.pourDrink("3f58dd75-bb21-11eb-8145-b831b5854dfb")
