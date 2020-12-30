"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ui import View, ShoppingList

from hotshopper.foodplan import FoodPlan


class Controller:

    def __init__(self, view):
        self.foodplan = FoodPlan()
        self.recipes = []
        self.view = view
        self.view.initialize(self.get_recipes(), self.foodplan)
        self.shopping_list = ShoppingList(self.view, self.get_ingredients())

    def get_recipes(self):
        recipes = [recipe for recipe in Recipe.__subclasses__()]
        return sorted(recipes, key=lambda recipe: recipe.name)

    def get_ingredients(self):
        self.foodplan.set_shopping_list(self.recipes)
        return self.foodplan.get_shopping_list()

    def create_shopping_list(self):
        if self.shopping_list is not None:
            self.shopping_list = ShoppingList(self.view, self.get_ingredients)


def main():
    view = View()
    Controller(view)
    view.mainloop()
