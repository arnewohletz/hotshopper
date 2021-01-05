"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ui import View, ShoppingListsFrame

from hotshopper.foodplan import FoodPlan


class Controller:

    def __init__(self, view):
        self.foodplan = FoodPlan()
        self.recipes = []
        self.view = view
        self.view.initialize(self, self.get_recipes())

    def get_recipes(self):
        recipes = [recipe for recipe in Recipe.__subclasses__()]
        return sorted(recipes, key=lambda recipe: recipe.name)

    def get_ingredients(self):
        self.foodplan.set_shopping_lists(self.recipes)
        return self.foodplan.get_shopping_lists()

    def display_shopping_lists(self, recipes):
        self.foodplan.set_shopping_lists(recipes)
        shopping_lists = self.foodplan.get_shopping_lists()
        self.view.display_shopping_lists(shopping_lists)


def main():
    view = View()
    Controller(view)
    view.mainloop()
