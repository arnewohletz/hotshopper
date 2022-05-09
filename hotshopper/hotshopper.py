"""Main module."""
from flask import render_template, redirect, session, request

from hotshopper.foodplan import FoodPlan
from hotshopper.model import Recipe, Ingredient, RecipeIngredient
from hotshopper.ui import View
from hotshopper import db, create_app


class Controller:
    def __init__(self, view=None):
        self.foodplan = None
        self.recipes = []
        self.ingredients = []
        if view:
            self.view = view
            self.view.initialize(self, self.get_recipes())

    def get_recipes(self):
        self.recipes = db.session.query(Recipe).all()
        return sorted(self.recipes, key=lambda recipe: recipe.name)

    def get_ingredients(self):
        self.ingredients = db.session.query(Ingredient).all()
        return sorted(self.ingredients, key=lambda ingredient: ingredient.name)
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
        ingredients = controller.get_ingredients()

        @app.route("/", methods=["GET", "POST"])
        def show_init_app():
            try:
                scroll_height = session.pop("scroll_height")
            except KeyError:
                scroll_height = 0
            # TODO: Add new recipes to main recipes:
            #   PROBLEM:
            #   Adding new recipe requires manual refresh
            #   SOLUTION:
            #   Compare 'recipes' and new set 'controller.get_recipes()'
            #   Don't change existing 'recipes', but only add additional ones
            #   found in 'controller.get_recipes() if any'
            #   NOTE:
            #   Ingredients can refresh via 'controller.get_ingredients()'
            #   if new ones were added, since those doesn't contain changed
            #   data
            return render_template("ontop_screens.html",
                                   recipes=recipes,
                                   ingredients=ingredients,
                                   # recipes=controller.get_recipes(),
                                   # ingredients=controller.get_ingredients(),
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
            return render_template("ontop_screens.html",
                                   recipes=recipes,
                                   food_plan=food_plan)

        @app.route("/delete_recipe/<int:recipe_id>")
        def delete_recipe(recipe_id):
            recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
            db.session.delete(recipe)
            db.session.commit()

        @app.route("/add_new_recipe/<int:amount_ingredients>", methods=["POST"])
        def add_new_recipe(amount_ingredients):
            name = request.form["recipe_name"]
            recipe = Recipe(name=name, ingredients=[])
            r_id = recipe.add()

            for j in range(amount_ingredients):
                ri_name = request.form[f"ingredient_{j}"]
                ri_unit = request.form[f"unit_{j}"]
                ri_quantity = request.form[f"quantity_{j}"]
                i_id = Ingredient.query.filter_by(name=ri_name).first().id
                ri = RecipeIngredient(recipe_id=r_id, ingredient_id=i_id,
                                      quantity_per_person=ri_quantity,
                                      unit=ri_unit)
                ri.add()

            db.session.commit()
            return redirect("/")

        app.run(port=port, debug=True)

    else:
        view = View()
        Controller(view)
        view.mainloop()
