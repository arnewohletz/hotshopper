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
        # self.shopping_list = ShoppingLists(self.view, self.get_ingredients())

    def get_recipes(self):
        recipes = [recipe for recipe in Recipe.__subclasses__()]
        return sorted(recipes, key=lambda recipe: recipe.name)

    # def set_shopping_lists(self):
    #     for recipe in self.recipes

    def get_ingredients(self):
        self.foodplan.set_shopping_lists(self.recipes)
        return self.foodplan.get_shopping_lists()

    def create_shopping_list(self):
        if self.shopping_list is not None:
            self.shopping_list = ShoppingListsFrame(self.view, self.get_ingredients())

    def display_shopping_lists(self, recipes):
        self.foodplan.set_shopping_lists(recipes)
        shopping_lists = self.foodplan.get_shopping_lists()
        self.view.display_shopping_lists(shopping_lists)
        # frm_shopping_lists = ShoppingListsFrame(self,
        #                                         self.foodplan.get_shopping_lists())
        # frm_shopping_lists.grid(column=1, row=0)


def main():
    view = View()
    Controller(view)
    view.mainloop()
