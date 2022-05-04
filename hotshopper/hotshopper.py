"""Main module."""
from flask import (render_template, redirect, session)

from hotshopper.foodplan import FoodPlan
from hotshopper.model import Recipe
from hotshopper.ui import View
from hotshopper import db, create_app


class Controller:
    def __init__(self, view=None):
        self.foodplan = None
        self.recipes = []
        if view:
            self.view = view
            self.view.initialize(self, self.get_recipes())

    def get_recipes(self):
        self.recipes = db.session.query(Recipe).all()
        return sorted(self.recipes, key=lambda recipe: recipe.name)

    # def get_recipe(self, recipe_id):
    #     for recipe in self.recipes:
    #         if recipe.
    #     return db.session.query(Recipe).filter_by(id=recipe_id)

    def display_shopping_lists(self):
        self.foodplan = FoodPlan()
        self.foodplan.set_shopping_lists(self.recipes)
        shopping_lists = self.foodplan.get_shopping_lists()
        self.view.display_shopping_lists(shopping_lists)


def main(web=True):

    if web:
        port = 5001
        app = create_app(test=False)

        controller = Controller()
        recipes = controller.get_recipes()

        @app.route("/")
        def show_init_app():
            try:
                scroll_height = session.pop("scroll_height")
            except KeyError:
                scroll_height = 0
            return render_template("foodplan.html", recipes=recipes,
                                   scroll_height=scroll_height)

        @app.route("/check_recipe/<recipe_id>_<int:week>_<int:scroll_height>")
        def check_recipe(recipe_id, week, scroll_height):
            for r in recipes:
                if r.id == int(recipe_id):
                    r.select(week)
                    session["scroll_height"] = scroll_height
                    return redirect("/")

        @app.route(
            "/uncheck_recipe/<recipe_id>_<int:week>_<int:scroll_height>")
        def uncheck_recipe(recipe_id, week, scroll_height):
            for i in recipes:
                if i.id == int(recipe_id):
                    i.unselect(week)
                    session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/show_shopping_list", methods=["POST"])
        def show_shopping_list():
            food_plan = FoodPlan()
            food_plan.set_shopping_lists(recipes)
            return render_template("foodplan.html",
                                   recipes=recipes,
                                   food_plan=food_plan)

        @app.route("/delete/<recipe_id>")
        def delete_recipe(recipe_id):
            recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
            db.session.delete(recipe)
            db.session.commit()

            # for i in recipes:
            #     if i.id == int(recipe_id):
            #         i.delete()

        app.run(port=port, debug=True)

    else:
        view = View()
        Controller(view)
        view.mainloop()
