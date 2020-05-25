"""Main module."""
import tkinter as tk
# from tkinter.ttk import Style
from hotshopper.recipes import Recipe
from hotshopper.ui import View, RecipeSelection, ShoppingList

from hotshopper.foodplan import FoodPlan
import hotshopper.recipes as rc


class Controller:

    def __init__(self, view: View):
        self.foodplan = FoodPlan()
        self.recipes = []
        # self.model = model
        self.view = view
        self.recipe_selection = RecipeSelection(self.view, self)
        self.shopping_list = ShoppingList(self.view, self)

    def get_recipes(self):
        for recipe in Recipe.__subclasses__():
            self.recipes.append(recipe())
        return self.recipes

    def get_ingredients(self):
        # self.recipes = []
        self.foodplan.set_shopping_list(self.recipes)
        return self.foodplan.get_shopping_list()
        # self.show_shopping_list()
        # return self.foodplan.shopping_list.get_ingredients()
        # TODO: Returns added ingredients of all selected recipes

    def create_shopping_list(self):
        # self.recipe_selection.destroy()
        # self.foodplan = None
        # self.foodplan = FoodPlan()
        # self.recipes = []
        if self.shopping_list is not None:
            # self.shopping_list.grid_forget()
            # self.shopping_list.destroy()
            self.shopping_list = ShoppingList(self.view, self)
        # self.view.switch_frame(ShoppingList)
        self.shopping_list.display()
        # (self.foodplan.get_shopping_list(), self))


# class RecipeCheckbutton:
#
#     def __init__(self, parent, recipe):
#         selected = tk.BooleanVar()
#         self.button = tk.Checkbutton(parent,
#                                      text=recipe.name,
#                                      variable=selected,
#                                      onvalue=True,
#                                      offvalue=False,
#                                      command=lambda: recipe.set_selected(
#                                          selected),
#                                      bg="#444",
#                                      fg="white")
#
#     def get(self):
#         return self.button
#
#
# class RecipeSelection(tk.Frame):
#
#     def __init__(self, parent):
#
#         tk.Frame.__init__(self, parent)
#         self.parent = parent
#         Style().configure("Hotshopper", background="#444")
#
#         all_recipes = []
#         recipes = rc.Recipe.__subclasses__()
#         # selected_recipes = []
#         food_plan = FoodPlan()
#
#         current_row = 1
#
#         for i in range(len(recipes)):
#             all_recipes.append(recipes[i]())
#
#         for recipe in all_recipes:
#             checkbutton = RecipeCheckbutton(self.parent, recipe)
#             checkbutton.get().grid(row=current_row, sticky="w")
#             current_row += 1
#
#         tk.Button(self.parent,
#                   text="Zutaten auflisten",
#                   fg="black",
#                   highlightbackground='#AAA',
#                   command=lambda: ShoppingList(all_recipes)).grid(row=current_row + 1)
#
#     def apply_to_shopping_list
#
# class ShoppingList(tk.Frame):
#
#     def __init__(self, recipes):
#


def main():
    # root = tk.Tk()
    # root.title("Hotshopper")
    # root.configure(background="#444")
    view = View()
    controller = Controller(view)
    view.intialize(controller)
    # TODO: View must not receive Controller instance
    # controller methods should be passed to View some other way
    # Also google again how to solve this
    view.mainloop()
