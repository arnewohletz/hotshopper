"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ui import View

from hotshopper.foodplan import FoodPlan

import random
import threading
import webbrowser

from flask import (Flask, render_template, request, redirect, make_response,
                   session
                   )


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
        # return f"Checked {recipe}"

    @app.route("/uncheck_recipe/<recipe>_<int:week>")
    def uncheck_recipe(recipe, week):
        for i in recipes:
            if i.__class__.__name__ == recipe:
                i.set_selected(False, week)
        return redirect("/")
        # return f"Checked {recipe}"

    @app.route("/show_shopping_list", methods=["POST"])
    def show_shopping_list():
        food_plan = FoodPlan()
        food_plan.set_shopping_lists(recipes)
        # for recipe in recipes:
        #     if recipe.selected:
        #         food_plan.
        #     for week in recipe.weeks:
        #         print(f"{recipe.name} selected for week {week}")

            # for week in range(1, 4):
            #     recipe_data = request.form[
            #         f"{recipe.__class__.__name__}_{week}"]
            #     print(recipe_data)
            # recipe_data = request.form[f"{recipe.name}_{week}"]

        return render_template("foodplan.html",
                               recipes=recipes,
                               food_plan=food_plan)

    return app
