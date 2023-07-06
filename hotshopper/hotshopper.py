"""Main module."""
import copy
from dataclasses import dataclass
from flask import render_template, redirect, session, request, make_response, \
    g, jsonify
import json
from sqlalchemy import func
from typing import List
from werkzeug.routing import IntegerConverter

from hotshopper.errors import (
    DuplicateIndexError,
    DuplicateIngredientError
)
from hotshopper import db, create_app
from hotshopper.constants import Unit
from hotshopper.foodplan import FoodPlan
from hotshopper.model import Recipe, Ingredient, RecipeIngredient, Location, \
    Section, ShoppingList
# from hotshopper.ui import View


class Controller:
    def __init__(self, view=None):
        # self.foodplan = None

        # location_supermarket = db.session.query(Location,
        #                                         name="Supermarkt").first()
        # location_market = db.session.query(Location, name="Markt").first()
        # location_bakery = db.session.query(Location, name="Bäckerei").first()
        # location_butcher = db.session.query(Location, name="Metzger").first()

        # self.existing_shopping_lists = db.session.query(ShoppingList).all()
        self.reset_shopping_lists()
        # supermarket_123 = ShoppingList(name="Supermarkt (Woche 1-3)",
        #                                locations=[Location.query.filter_by(name="Supermarkt").first()],
        #                                weeks=[1,2,3], print_columns=4)
        # market_1 = ShoppingList(name="Markt - Woche 1",
        #                         locations=[Location.query.filter_by(name="Markt").first(),
        #                                    Location.query.filter_by(name="Metzger").first(),
        #                                    Location.query.filter_by(name="Bäckerei").first()],
        #                         weeks=[1], print_columns=1)
        # market_2 = ShoppingList(name="Markt - Woche 2",
        #                         locations=[Location.query.filter_by(name="Markt").first(),
        #                                    Location.query.filter_by(name="Metzger").first(),
        #                                    Location.query.filter_by(name="Bäckerei").first()],
        #                         weeks=[2], print_columns=1)
        # market_3 = ShoppingList(name="Markt - Woche 3",
        #                         locations=[Location.query.filter_by(name="Markt").first(),
        #                                    Location.query.filter_by(name="Metzger").first(),
        #                                    Location.query.filter_by(name="Bäckerei").first()],
        #                         weeks=[3], print_columns=1)
        #
        # self.shopping_lists = [supermarket_123, market_1, market_2, market_3]
        # for shopping_list in self.existing_shopping_lists:
        #     self.shopping_lists.append(shopping_list.__class__(shopping_list.locations))
            # self.shopping_lists.append(ShoppingList(shopping_list.name,
            #     db.relationship("Location", secondary="shopping_list_location",
            #                 back_populates="shopping_lists")))
            # for location in shopping_list.locations_association:
            #     shopping_list.locations_association.append(location)
            # shopping_list.locations_association.append(
            #     ShoppingList(name=shopping_list.name,
            #                  # locations=shopping_list.locations,
            #                  print_columns=shopping_list.print_columns))

        # self.shopping_lists = [ShoppingList(locations=location_supermarket,
        #                                     name="Supermarkt Woche 1-3",
        #                                     weeks=1),
        #                        ShoppingList(locations=[location_butcher,
        #                                                location_bakery,
        #                                                location_market],
        #                                     name="Markt - Woche 1"),
        #                        ShoppingList(locations=[location_butcher,
        #                                                location_bakery,
        #                                                location_market],
        #                                     name="Markt - Woche 2"),
        #                        ShoppingList(locations=[location_butcher,
        #                                                location_bakery,
        #                                                location_market],
        #                                     name="Markt - Woche 3"),
        #                        ]

        # self.shopping_lists = db.session.query(ShoppingList).all()
        self.foodplan = FoodPlan(self.shopping_lists)
        # self.shopping_lists = None
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

    @staticmethod
    def get_ingredient(name):
        ingredient = db.session.query(Ingredient).filter_by(name=name).first()
        return ingredient

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

    def get_shopping_lists(self):
        return self.foodplan.shopping_lists

    @staticmethod
    def get_always_on_list_items(location_id):
        items = Ingredient.query.filter_by(id=location_id,
                                           always_on_list=1).all()
        return items

    def get_food_plan(self):
        return self.foodplan

    def reset_shopping_lists(self):
        supermarket_123 = ShoppingList(name="Supermarkt (Woche 1-3)",
                                       locations=[Location.query.filter_by(
                                           name="Supermarkt").first()],
                                       weeks=[1, 2, 3], print_columns=4)
        market_1 = ShoppingList(name="Markt - Woche 1",
                                locations=[Location.query.filter_by(
                                    name="Markt").first(),
                                           Location.query.filter_by(
                                               name="Metzger").first(),
                                           Location.query.filter_by(
                                               name="Bäckerei").first()],
                                weeks=[1], print_columns=1)
        market_2 = ShoppingList(name="Markt - Woche 2",
                                locations=[Location.query.filter_by(
                                    name="Markt").first(),
                                           Location.query.filter_by(
                                               name="Metzger").first(),
                                           Location.query.filter_by(
                                               name="Bäckerei").first()],
                                weeks=[2], print_columns=1)
        market_3 = ShoppingList(name="Markt - Woche 3",
                                locations=[Location.query.filter_by(
                                    name="Markt").first(),
                                           Location.query.filter_by(
                                               name="Metzger").first(),
                                           Location.query.filter_by(
                                               name="Bäckerei").first()],
                                weeks=[3], print_columns=1)

        self.shopping_lists = [supermarket_123, market_1, market_2, market_3]
        # self.shopping_lists = db.session.query(ShoppingList).all()

    def display_shopping_lists(self):
        # self.foodplan = FoodPlan()
        self.foodplan.set_shopping_lists(self.recipes)
        # self.shopping_lists = self.foodplan.get_shopping_lists()
        self.view.display_shopping_lists(self.shopping_lists)

    @staticmethod
    def get_highest_order_id(model: db.Model, **filters):
        result = \
            db.session.query(model, func.max(model.order_id)).filter_by(
                **filters)[
                0][1]
        if result:
            return result
        else:
            return 0

    @staticmethod
    def get_section_id(location_id, order_id):
        if order_id == -1:
            return order_id
        result = Section.query.filter_by(location_id=location_id,
                                         order_id=order_id).first()
        return result.id


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'


def main(web=True):
    if web:
        port = 5002
        app = create_app(test=False)
        app.url_map.converters['signed_int'] = SignedIntConverter
        controller = Controller()

        # food_plan = None

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
        @app.route("/shopping_list/<int:scroll_height>")
        def show_shopping_list_screen(scroll_height=None):
            ingredients = controller.get_ingredients()
            recipes = controller.get_recipes()
            locations = controller.get_locations()
            return render_template("shopping_list.html",
                                   locations=locations,
                                   ingredients=ingredients,
                                   recipes=recipes,
                                   scroll_height=scroll_height)

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

        @app.route("/show_shopping_list", methods=["POST", "GET"])
        def show_shopping_list():
            controller.reset_shopping_lists()
            recipes = controller.get_recipes()
            # nonlocal food_plan
            food_plan = FoodPlan(controller.shopping_lists)
            food_plan.set_shopping_lists(recipes)
            # g.food_plan = food_plan
            controller.foodplan = food_plan
            # TODO: Ingredients must be sorted via order_id (also sections
            #  and locations)
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

        @app.route("/edit_recipe/<int:recipe_id>")
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

        @app.route("/print_shopping_list", methods=["POST"])
        def print_shopping_list():
            food_plan = controller.foodplan
            return render_template("print_shopping_list.html",
                                   food_plan=food_plan)

        @app.route(
            "/confirm_edit_recipe/<int:recipe_id>_<int:amount_ingredients>_"
            "<int:scroll_height>",
            methods=["POST"])
        def confirm_edit_recipe(recipe_id, amount_ingredients, scroll_height):

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

        # @app.route("/add_ingredient/<int:location_id>")
        # def add_ingredient_old(location_id):
        #     return render_template("add_ingredient_screen.html",
        #                            ingredients=controller.get_ingredients(),
        #                            locations=controller.get_locations(),
        #                            sections=controller.get_sections(
        #                                location_id)
        #                            )

        @app.route("/ingredients/new")
        def show_add_ingredient_screen():
            # edit = bool(request.args.get("edit"))
            # if edit:
            #     ingredients = Ingredient.query.filter_by(
            #         id=ingredient_id).all()
            #     if len(ingredients) > 1:
            #         raise DuplicateIndexError(
            #             f"Index '{id}' is used more than once."
            #             f"Also used by {[i.name for i in ingredients]}")
            #     result = ingredients[0]
            #     return render_template("add_ingredient_screen.html",
            #                            recipes=controller.get_recipes(),
            #                            ingredients=controller.get_ingredients(),
            #                            locations=controller.get_locations(),
            #                            ingredient=result)
            return render_template("add_ingredient_screen.html",
                                   recipes=controller.get_recipes(),
                                   ingredients=controller.get_ingredients(),
                                   locations=controller.get_locations(),
                                   location=None
                                   )

        @app.route("/ingredients/edit/<int:ingredient_id>")
        def show_edit_ingredient_screen(ingredient_id):
            ingredients = Ingredient.query.filter_by(id=ingredient_id).all()
            if len(ingredients) > 1:
                raise DuplicateIndexError(
                    f"Index '{id}' is used more than once."
                    f"Also used by {[i.name for i in ingredients]}")
            ingredient = ingredients[0]
            section = Section.query.filter_by(id=ingredient.section_id).first()
            location = Location.query.filter_by(id=section.location_id).first()
            return render_template("edit_ingredient_screen.html",
                                   recipes=controller.get_recipes(),
                                   ingredients=controller.get_ingredients(),
                                   locations=controller.get_locations(),
                                   ingredient=ingredient,
                                   location=location,
                                   section=section
                                   )

        @app.route("/ingredients/delete/<int:ingredient_id>")
        def delete_ingredient(ingredient_id):
            ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
            ingredient.delete()
            return redirect("/ingredients")

        @app.route(
            "/confirm_new_ingredient/<int:location_id>_<signed_int"
            ":section_order_id>_<string:non_food>",
            methods=["POST", "GET"])
        def add_ingredient(location_id, section_order_id, non_food):

            def bool_to_int(s: str) -> int:
                if s.lower() == "true":
                    return 1
                elif s.lower() == "false":
                    return 0
                else:
                    var_name = f'{s=}'.split('=')[0]
                    raise ValueError(f"'{var_name}' has illegal value: ${s}")

            # data = request
            form = json.loads(str(request.data, "utf-8"))
            name = form["ingredient_name"]
            always_on_list = bool_to_int(form["always_on_list"])
            section_id = controller.get_section_id(location_id,
                                                   section_order_id)
            current_max_order_id = controller.get_highest_order_id(Ingredient,
                                                                   section_id=section_id)

            i = Ingredient(name=name, always_on_list=always_on_list,
                           location_id=location_id,
                           section_id=section_id,
                           non_food=bool_to_int(non_food),
                           order_id=current_max_order_id + 1)

            try:
                i.add()
            except DuplicateIngredientError:
                response = make_response()
                response.status = 409
                response.header = "Duplicate Ingredient Error"
                return response

            return redirect("/ingredients")

        @app.route("/confirm_edit_ingredient/"
                   "<int:ingredient_id>_"
                   "<int:location_id>_"
                   "<signed_int:section_order_id>_"
                   "<string:non_food>", methods=["POST", "GET"])
        def confirm_edit_ingredient(ingredient_id, location_id, section_order_id, non_food):

            def bool_to_int(s: str) -> int:
                if s.lower() == "true":
                    return 1
                elif s.lower() == "false":
                    return 0
                else:
                    var_name = f'{s=}'.split('=')[0]
                    raise ValueError(f"'{var_name}' has illegal value: ${s}")

            form = json.loads(str(request.data, "utf-8"))
            name = form["ingredient_name"]

            always_on_list = bool_to_int(form["always_on_list"])
            section_id = controller.get_section_id(location_id,
                                                   section_order_id)

            existing_ingredient = Ingredient.query.filter_by(id=ingredient_id).first()

            # if location_id != existing_ingredient.location_id \
            #     or section_id is not existing_ingredient.section_id:
            #
            #     section_order_id = controller.get_highest_order_id(Ingredient,
            #                                                section_id=section_id)

            try:
                # TODO: add update method to Ingredient model class
                existing_ingredient.name = name
                existing_ingredient.location_id = location_id
                existing_ingredient.order_id = section_order_id
                existing_ingredient.section_id = section_id
                existing_ingredient.always_on_list = always_on_list
                existing_ingredient.non_food = bool_to_int(non_food)

                db.session.commit()
                # TODO: UPDATE DOES NOT WORK! NOT WRITTEN TO DATABASE

            except DuplicateIngredientError:
                response = make_response()
                response.status = 409
                response.header = "Duplicate Ingredient Error"
                return response

            return redirect("/ingredients")



        @app.route(
            "/update_ingredient_order/<int:location_id>/<int:section_id"
            ">/<string:new_ingr_id_order>/<int:scroll_height>")
        def set_new_ingredient_order(location_id, section_id,
                                     new_ingr_id_order, scroll_height):
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
            return redirect(f"/shopping_list/{scroll_height}")

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
            "/update_section_order/<int:location_id>/<string"
            ":new_sec_id_order>")
        def set_new_section_order(location_id, new_sec_id_order):
            # TODO: Implement update section order
            return redirect(f"/shopping_list/edit/{location_id}")

            # for i, new in enumerate(new_ingr_id_order):
            #     if int(new) == current_ingr_id_order[i]:
            #         continue
            #     else:
            #         Ingredient.query.filter_by(section_id=section_id,
            #                                    order_id=i).first(
            #                                    ).update_order_id(
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

            # TODO: Find another way to end function -> refresh
            #  /shopping_list sucks
            return redirect("/shopping_list")

        app.run(port=port, debug=True)

    # else:
    #     view = View()
    #     Controller(view)
    #     view.mainloop()
