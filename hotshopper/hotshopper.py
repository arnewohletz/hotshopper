"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ui import View

from hotshopper.foodplan import FoodPlan

import random
import threading
import webbrowser

from flask import Flask, render_template, request, redirect


# class Controller:
#     def __init__(self, view):
#         self.foodplan = None
#         self.recipes = []
#         self.view = view
#         self.view.initialize(self, self.get_recipes())
#
#     def get_recipes(self):
#         self.recipes = [recipe() for recipe in Recipe.__subclasses__()]
#         return sorted(self.recipes, key=lambda recipe: recipe.name)
#
#     def display_shopping_lists(self):
#         self.foodplan = FoodPlan()
#         self.foodplan.set_shopping_lists(self.recipes)
#         shopping_lists = self.foodplan.get_shopping_lists()
#         self.view.display_shopping_lists(shopping_lists)


class Controller:
    def __init__(self):
        self.foodplan = None
        self.recipes = []
        # self.view = view

    def get_recipes(self):
        self.recipes = [recipe() for recipe in Recipe.__subclasses__()]
        return sorted(self.recipes, key=lambda recipe: recipe.name)


def main(autostart=False, debug=True):

    app = Flask(__name__)

    # Controller(app)

    # view = View()
    # Controller(view)
    # view.mainloop()
    controller = Controller()
    recipes = controller.get_recipes()

    # def run():
    #     app.run(port=port, debug=debug)

    @app.route("/")
    def show_init_app():
        return render_template("foodplan.html", recipes=recipes)

    @app.route("/check_recipe/<recipe>_<int:week>")
    def check_recipe(recipe, week):
        for i in recipes:
            if i.__class__.__name__ == recipe:
                i.set_selected(True, week)
        return redirect("/")

    @app.route("/uncheck_recipe/<recipe>_<int:week>")
    def uncheck_recipe(recipe, week):
        for i in recipes:
            if i.__class__.__name__ == recipe:
                i.set_selected(False, week)
        return redirect("/")

    @app.route("/get_shopping_list", methods=["POST"])
    def show_shopping_list():
        recipes_data = request.form.get("recipe_selection")
        return None

    return app
