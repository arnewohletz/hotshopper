"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ui import View

from hotshopper.foodplan import FoodPlan


class Controller:
    def __init__(self, view):
        self.foodplan = None
        self.recipes = []
        self.view = view
        self.view.initialize(self, self.get_recipes())

    def get_recipes(self):
        self.recipes = [recipe() for recipe in Recipe.__subclasses__()]
        return sorted(self.recipes, key=lambda recipe: recipe.name)

    def display_shopping_lists(self):
        self.foodplan = FoodPlan()
        self.foodplan.set_shopping_lists(self.recipes)
        shopping_lists = self.foodplan.get_shopping_lists()
        self.view.display_shopping_lists(shopping_lists)


def main():
    view = View()
    Controller(view)
    view.mainloop()
