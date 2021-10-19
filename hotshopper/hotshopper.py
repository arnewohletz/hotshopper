"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ui import View

from hotshopper.foodplan import FoodPlan

import random
import threading
import webbrowser
import secrets


from flask import (Flask, render_template, request, redirect, make_response,
                   session
                   )


class Controller:
    def __init__(self, view=None):
        self.foodplan = None
        self.recipes = []
        if view:
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


# class Controller:
#     def __init__(self, view=None):
#         self.foodplan = None
#         self.recipes = []
#         if view:
#             self.view = view
#
#     def get_recipes(self):
#         self.recipes = [recipe() for recipe in Recipe.__subclasses__()]
#         return sorted(self.recipes, key=lambda recipe: recipe.name)


def main(web=True):
    app = None
    controller = Controller()
    recipes = controller.get_recipes()

    # Controller(app)
    # view = View()
    # Controller(view)
    # view.mainloop()

    if web:
        app = Flask(__name__)
        app.secret_key = secrets.token_hex()
        port = 5001

        @app.route("/")
        def show_init_app():
            try:
                scroll_height = session.pop("scroll_height")
            except KeyError:
                scroll_height = 0
            return render_template("foodplan.html", recipes=recipes,
                                   scroll_height=scroll_height)

        @app.route("/check_recipe/<recipe>_<int:week>_<int:scroll_height>")
        def check_recipe(recipe, week, scroll_height):
            for i in recipes:
                if i.__class__.__name__ == recipe:
                    i.set_selected(True, week)
                    session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/uncheck_recipe/<recipe>_<int:week>_<int:scroll_height>")
        def uncheck_recipe(recipe, week, scroll_height):
            for i in recipes:
                if i.__class__.__name__ == recipe:
                    i.set_selected(False, week)
                    session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/show_shopping_list", methods=["POST"])
        def show_shopping_list():
            food_plan = FoodPlan()
            food_plan.set_shopping_lists(recipes)
            return render_template("foodplan.html",
                                   recipes=recipes,
                                   food_plan=food_plan)

        app.run(port=port, debug=True)

    else:
        view = View()
        Controller(view)
        view.mainloop()

