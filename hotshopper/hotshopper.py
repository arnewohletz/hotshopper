"""Main module."""
from flask import render_template, redirect, session, request

from hotshopper.constants import Unit
from hotshopper.foodplan import FoodPlan
from hotshopper.model import Recipe, Ingredient, RecipeIngredient, Location, \
    Section
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
        return sorted(self.recipes, key=lambda recipe: recipe.name.lower())

    def get_ingredients(self):
        self.ingredients = db.session.query(Ingredient).all()
        return sorted(self.ingredients,
                      key=lambda ingredient: ingredient.name.lower())

    @staticmethod
    def get_sections(location_id):
        sections = db.session.query(Section).filter_by(
            location_id=location_id).all()
        return sorted(sections, key=lambda section: section.order_id)

    @staticmethod
    def get_recipe(recipe_id: int):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        return recipe

    @staticmethod
    def get_recipe_ingredients(recipe_id: int):
        ris = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
        return ris

    @staticmethod
    def get_locations():
        ls = Location.query.all()
        return sorted(ls, key=lambda location: location.order_id)

    @staticmethod
    def get_location(location_id):
        loc = Location.query.filter_by(id=location_id).first()
        return loc

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

        @app.route("/", methods=["GET", "POST"])
        def show_init_app():
            try:
                scroll_height = session.pop("scroll_height")
            except KeyError:
                scroll_height = 0
            return render_template("main_screen.html",
                                   recipes=controller.get_recipes(),
                                   scroll_height=scroll_height)

        @app.route("/ingredients")
        def show_ingredients():
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            return render_template("ingredients.html", ingredients=ingredients,
                                   recipes=recipes)

        @app.route("/shopping_list")
        def show_shopping_list_screen():
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            locations = controller.get_locations()
            # TODO: Ingredients must be sorted via order_id (also sections and locations)
            return render_template("shopping_list.html",
                                   locations=locations,
                                   ingredients=ingredients,
                                   recipes=recipes)

        @app.route("/shopping_list/edit")
        def show_shopping_list_edit_screen():
            locations = controller.get_locations()
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            return render_template("edit_shopping_list.html",
                                   locations=locations,
                                   ingredients=ingredients,
                                   selected_location=None,
                                   recipes=recipes)

        @app.route("/shopping_list/edit/<int:location_id>")
        def show_section_edit_screen(location_id):
            locations = controller.get_locations()
            selected_location = controller.get_location(location_id)
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            return render_template("edit_shopping_list.html",
                                   locations=locations,
                                   selected_location=selected_location,
                                   ingredients=ingredients,
                                   recipes=recipes)

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
            recipes = controller.get_recipes()
            food_plan = FoodPlan()
            food_plan.set_shopping_lists(recipes)
            return render_template("main_screen.html",
                                   recipes=recipes,
                                   food_plan=food_plan)

        @app.route("/add_recipe")
        def show_add_recipe_screen():
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            return render_template("add_recipe_screen.html",
                                   recipes=recipes,
                                   ingredients=ingredients,
                                   unit=Unit)

        @app.route("/edit_recipe/<int:recipe_id>", methods=["POST", "GET"])
        def show_edit_recipe_screen(recipe_id):
            recipes = controller.get_recipes()
            recipe = controller.get_recipe(recipe_id)
            recipe_ingredients = controller.get_recipe_ingredients(recipe_id)
            return render_template("edit_recipe_screen.html",
                                   recipes=recipes,
                                   recipe=recipe,
                                   recipe_ingredients=recipe_ingredients,
                                   ingredients=controller.get_ingredients(),
                                   unit=Unit
                                   )

        @app.route(
            "/confirm_edit_recipe/<int:recipe_id>_<int:amount_ingredients>_<int:scroll_height>",
            methods=["POST"])
        def edit_recipe(recipe_id, amount_ingredients, scroll_height):

            r_name = request.form[f"recipe_name"]
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            recipe.update(r_name)

            all_ingredients = RecipeIngredient.query.filter_by(
                recipe_id=recipe_id).all()
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
            session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route("/delete_recipe/<int:recipe_id>_<int:scroll_height>")
        def delete_recipe(recipe_id, scroll_height):
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            recipe.delete()
            session["scroll_height"] = scroll_height
            return redirect("/")

        @app.route(
            "/confirm_new_recipe/<int:amount_ingredients>_<int:scroll_height>",
            methods=["POST", "GET"])
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
            return redirect("/")

        @app.route("/add_ingredient/<int:location_id>")
        def add_ingredient(location_id):
            return render_template("add_ingredient_screen.html",
                                   ingredients=controller.get_ingredients(),
                                   locations=controller.get_locations(),
                                   sections=controller.get_sections(
                                       location_id)
                                   )

        @app.route(
            "/update_ingredient_order/<int:location_id>/<int:section_id>/<string:new_ingr_id_order>")
        def set_new_ingredient_order(location_id, section_id,
                                     new_ingr_id_order):
            new_ingr_id_order = new_ingr_id_order.split("_")
            section = Section.query.filter_by(location_id=location_id,
                                              id=section_id).first()
            ingredients = section.get_ingredients()
            current_ingr_id_order = [i.id for i in ingredients]
            # ingredients = Ingredient.query.filter_by(
            #     section_id=section_id).all()
            for i in range(len(new_ingr_id_order)):
                if new_ingr_id_order[i] == current_ingr_id_order[i]:
                    continue
                else:
                    Ingredient.query.filter_by(
                        id=new_ingr_id_order[i]).first().update_order_id(i)
            return redirect("/shopping_list")

        @app.route("/update_location_order/<string:new_loc_id_order>")
        def set_new_location_order(new_loc_id_order):
            new_loc_id_order = new_loc_id_order.split("_")
            locations = controller.get_locations()
            current_loc_id_order = [i.id for i in locations]

            for i in range(len(new_loc_id_order)):
                if new_loc_id_order[i] == current_loc_id_order[i]:
                    continue
                else:
                    Location.query.filter_by(
                        id=new_loc_id_order[i]).first().update_order_id(i)

            return redirect("/shopping_list/edit")

        @app.route(
            "/update_section_order/<int:location_id>/<string:new_sec_id_order>")
        def set_new_section_order(location_id, new_sec_id_order):
            # TODO: Implement update section order
            return redirect(f"/shopping_list/edit/{location_id}")

            # for i, new in enumerate(new_ingr_id_order):
            #     if int(new) == current_ingr_id_order[i]:
            #         continue
            #     else:
            #         Ingredient.query.filter_by(section_id=section_id,
            #                                    order_id=i).first().update_order_id(
            #             int(new))

            # for i, ingredient in enumerate(ingredients, start=0):
            #     if ingredient.order_id == int(new_ingr_id_order[i]):
            #         continue
            #     else:
            #         Ingredient.query.filter_by(section_id=section_id,
            #                                    order_id=ingredient.order_id).first().update_order_id(
            #             new_ingr_id_order[i])
            # db.session.query(Ingredient).filter(
            #     Ingredient.section_id == int(section_id),
            #     Ingredient.order_id == int(current_order_id)).update(
            #     {"order_id": new_order_id}, synchronize_session=False)
            # ingredients = Ingredient.query.filter_by(
            #     section_id=section_id).all()
            db.session.commit()

            # TODO: Find another way to end function -> refresh /shopping_list sucks
            return redirect("/shopping_list")

        app.run(port=port, debug=True)

    else:
        view = View()
        Controller(view)
        view.mainloop()
