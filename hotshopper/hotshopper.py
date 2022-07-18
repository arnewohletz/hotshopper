"""Main module."""
from flask import render_template, redirect, session, request

from hotshopper.foodplan import FoodPlan
from hotshopper.model import Recipe, Ingredient, RecipeIngredient
from hotshopper.ui import View
from hotshopper import db, create_app


class Controller:
    def __init__(self, view=None):
        self.foodplan = None
        self.recipes = []  # make to set() ??
        self.ingredients = []
        if view:
            self.view = view
            self.view.initialize(self, self.get_recipes())

    def get_recipes(self):
        all_recipes = db.session.query(Recipe).all()
        for recipe in all_recipes:
            if recipe not in self.recipes:
                self.recipes.append(recipe)
        for recipe in self.recipes:
            if recipe not in all_recipes:
                self.recipes.remove(recipe)
        return sorted(self.recipes, key=lambda recipe: recipe.name)

    def get_ingredients(self):
        self.ingredients = db.session.query(Ingredient).all()
        return sorted(self.ingredients, key=lambda ingredient: ingredient.name)

    @staticmethod
    def get_recipe(recipe_id: int):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        return recipe

    @staticmethod
    def get_recipe_ingredients(recipe_id: int):
        ris = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
        return ris

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
        # if "recipes" not in session:
        #     session["recipes"] = controller.get_recipes()
        recipes = controller.get_recipes()

        # ingredients = controller.get_ingredients()

        @app.route("/", methods=["GET", "POST"])
        def show_init_app():
            try:
                scroll_height = session.pop("scroll_height")
            except KeyError:
                scroll_height = 0
            # nonlocal recipes, ingredients
            return render_template("main_screen.html",
                                   recipes=controller.get_recipes(),
                                   # ingredients=controller.get_ingredients(),
                                   scroll_height=scroll_height)
            # return render_template("add_recipe_screen.html",
            #                        recipes=controller.get_recipes(),
            #                        ingredients=controller.get_ingredients(),
            #                        scroll_height=scroll_height)

        @app.route("/check_recipe/<recipe_id>_<int:week>_<int:scroll_height>")
        def check_recipe(recipe_id, week, scroll_height):
            for r in controller.get_recipes():
                if r.id == int(recipe_id):
                    r.select(week)
                    session["scroll_height"] = scroll_height
                    return redirect("/")

        @app.route(
            "/uncheck_recipe/<recipe_id>_<int:week>_<int:scroll_height>")
        def uncheck_recipe(recipe_id, week, scroll_height):
            for i in controller.get_recipes():
                if i.id == int(recipe_id):
                    i.unselect(week)
                    session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/show_shopping_list", methods=["POST"])
        def show_shopping_list():
            # recipes = controller.recipes
            r = controller.get_recipes()
            food_plan = FoodPlan()
            food_plan.set_shopping_lists(r)
            return render_template("main_screen.html",
                                   recipes=r,
                                   # recipes=controller.get_recipes(),
                                   food_plan=food_plan)

        @app.route("/add_recipe")
        def show_add_recipe_screen():
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            return render_template("add_recipe_screen.html",
                                   recipes=recipes,
                                   ingredients=ingredients)

        @app.route("/edit_recipe/<int:recipe_id>", methods=["POST", "GET"])
        def show_edit_recipe_screen(recipe_id):
            recipes = controller.get_recipes()
            recipe = controller.get_recipe(recipe_id)
            recipe_ingredients = controller.get_recipe_ingredients(recipe_id)
            return render_template("edit_recipe_screen.html",
                            recipes=recipes,
                            recipe=recipe,
                            recipe_ingredients=recipe_ingredients,
                            ingredients=controller.get_ingredients())

        @app.route("/confirm_edit_recipe/<int:recipe_id>_<int:amount_ingredients>_<int:scroll_height>", methods=["POST"])
        def edit_recipe(recipe_id, amount_ingredients, scroll_height):

            r_name = request.form[f"recipe_name"]
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            recipe.update(r_name)

            all_ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
            for ingredient in all_ingredients:
                ingredient.delete()

            for j in range(amount_ingredients):
                ri_unit = request.form[f"unit_{j}"]
                ri_quantity = float(request.form[f"quantity_{j}"])
                ri_name = request.form[f"ingredient_{j}"]
                i_id = Ingredient.query.filter_by(name=ri_name).first().id

                ri = RecipeIngredient(recipe_id=recipe_id,
                                      ingredient_id=i_id,
                                      quantity_per_person=ri_quantity,
                                      unit=ri_unit)
                ri.add()

            db.session.expire_on_commit = False
            db.session.commit()
            # session["recipes"] = controller.get_recipes()
            # recipes = controller.get_recipes()
            session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/delete_recipe/<int:recipe_id>_<int:scroll_height>")
        def delete_recipe(recipe_id, scroll_height):
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            recipe.delete()
            session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/confirm_new_recipe/<int:amount_ingredients>_<int:scroll_height>", methods=["POST", "GET"])
        def add_new_recipe(amount_ingredients, scroll_height):
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

            db.session.expire_on_commit = False
            db.session.commit()
            session["scroll_height"] = scroll_height
            # session["recipes"] = controller.get_recipes()
            return redirect("/")

        app.run(port=port, debug=True)

    else:
        view = View()
        Controller(view)
        view.mainloop()
