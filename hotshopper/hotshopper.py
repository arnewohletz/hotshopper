
"""Main module."""

# Standard library imports
import json

# Third-party imports
from flask import (
    make_response,
    redirect,
    render_template,
    request,
    session
)
from sqlalchemy import func
from typing import (
    List,
    Type
)
from werkzeug.routing import IntegerConverter
from werkzeug.wrappers import Response as BaseResponse

# Intra-package imports
from hotshopper.helper import Helper
from hotshopper import get_app, get_db
from hotshopper.errors import (
    DuplicateIndexError,
    DuplicateIngredientError
)
from hotshopper.foodplan import FoodPlan
from hotshopper.model import (
    Ingredient,
    Location,
    OrderedModel,
    Recipe,
    RecipeIngredient,
    Section,
    ShoppingList,
    Unit
)


class Controller:
    """
    Access controller for the database data.
    """
    def __init__(self):
        self.db = get_db()
        self.food_plan = FoodPlan(self.get_shopping_lists())
        self.recipes = []
        self.ingredients = []

    def get_recipes(self) -> list:
        """
        Get all recipes from the database, maintaining the state of preexisting recipes.
        """
        all_recipes = self.db.session.query(Recipe).all()
        for recipe in all_recipes:
            if recipe not in self.recipes:
                self.recipes.append(recipe)
        for recipe in self.recipes:
            if recipe not in all_recipes:
                self.recipes.remove(recipe)
        return sorted(self.recipes, key=lambda r: r.name.lower())

    def get_shopping_lists(self) -> list:
        """
        Get all shopping lists from the database.
        """
        return self.db.session.query(ShoppingList).all()

    def get_ingredients(self) -> list:
        """
        Get all ingredients from the database.
        """
        self.ingredients = self.db.session.query(Ingredient).all()
        return sorted(self.ingredients,
                      key=lambda ingredient: ingredient.name.lower())

    def get_food_only_ingredients(self):
        self.ingredients = Ingredient.query.filter(Ingredient.non_food == 0).all()
        return sorted(self.ingredients,
                      key=lambda ingredient: ingredient.name.lower())

    @staticmethod
    def get_recipe(recipe_id: int) -> Recipe:
        """
        Get single recipe which matches the given :param:`recipe_id`.

        :param recipe_id: Primary integer key of the recipe.
        """
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        return recipe

    @staticmethod
    def get_recipe_ingredients(recipe_id: int) -> List[RecipeIngredient]:
        """
        Get all RecipeIngredients of the Recipe matching the given :param:`recipe_id`.

        :param recipe_id: Primary integer key of the recipe.
        """
        ris = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()
        return ris

    @staticmethod
    def get_locations() -> List[Location]:
        """
        Get all locations from the database
        """
        ls = Location.query.all()
        return sorted(ls, key=lambda location: location.order_id)

    @staticmethod
    def get_location(location_id) -> Location:
        """
        Get Location object which matches the given :param:`location_id`.
        """
        loc = Location.query.filter_by(id=location_id).first()
        return loc

    @staticmethod
    def get_sections(location_id) -> List[Section]:
        """
        Get all Sections objects associated with the matching :param:`location_id`.
        """
        secs = Section.query.filter_by(location_id=location_id).all()
        return sorted(secs, key=lambda section: section.order_id)

    @staticmethod
    def get_always_on_list_items(location_id: int) -> List[Ingredient]:
        """
        Get all items for given :param:`location_id` which must always be on the shopping list.

        :param location_id: The primary integer key of the location.
        """
        items = Ingredient.query.filter_by(id=location_id,
                                           always_on_list=1).all()
        return items

    def get_highest_order_id(self, model: Type[OrderedModel], **filters) -> int:
        """
        Return the highest order ID for a :param:`model`'s database data.

        :param model: A class type of OrderedModel to query.
        :param filters: Dictionary of filters to apply
        """
        result = self.db.session.query(
            model, func.max(model.order_id)).filter_by(**filters)[0][1]
        if result:
            return result
        else:
            return 0

    @staticmethod
    def get_section_id(location_id: int, order_id: int) -> int:
        """
        Return the section ID for a :type:`Section` database entry which
        matches the given :param:`location_id` and :param:`order_id`.

        :param location_id: The primary integer key of the location.
        :param order_id: The primary integer key of the order.
        """
        if order_id == -1:
            return order_id
        result = Section.query.filter_by(location_id=location_id,
                                         order_id=order_id).first()
        return result.id


class SignedIntConverter(IntegerConverter):
    """
    Provides support for signed integer conversion for Werkzeug URL routing

    Example:
    app = Flask(__name__)
    app.url_map.converters['signed_int'] = SignedIntConverter

    @app.route("/add/<signed_int:integer_1>_<signed_int:integer_2>")
    def add(integer_1, integer_2):
        // do calculation ...
    """
    regex = r'-?\d+'


def main() -> None:
    """
    Main entry point for hotshopper.
    """
    port = 5002
    app = get_app()
    app.url_map.converters['signed_int'] = SignedIntConverter
    controller = Controller()

    @app.route("/", methods=["GET"])  # remove 'POST' - see if it causes issues
    def show_main_page() -> str:
        """
        Returns the rendered main page of the application.

        It handles displaying the main screen of the application, which
        includes a list of defined recipes and various control elements.
        It applies the scroll height of the session to maintain the user's
        current scroll position.
        """
        try:
            scroll_height = session.pop("scroll_height")
        except KeyError:
            scroll_height = 0
        return render_template("main_screen.html",
                               recipes=controller.get_recipes(),
                               scroll_height=scroll_height)

    @app.route("/ingredients")
    def show_ingredients() -> str:
        """
        Returns the rendered ingredients page.

        The ingredients page is displayed on top of the main screen and
        shows a list of all :type:`Ingredient` data rows that are saved
        in the database.
        """
        ingredients = controller.get_ingredients()
        recipes = controller.get_recipes()
        return render_template("ingredients.html", ingredients=ingredients,
                               recipes=recipes)

    @app.route("/shopping_list/<int:scroll_height>")
    def show_shopping_list_screen(scroll_height: int) -> str:
        """
        RReturns the rendered shopping list page.

        :param scroll_height: The current scroll height of the shopping list page.
        """
        ingredients = controller.get_ingredients()
        recipes = controller.get_recipes()
        locations = controller.get_locations()
        return render_template("shopping_list.html",
                               locations=locations,
                               ingredients=ingredients,
                               recipes=recipes,
                               scroll_height=scroll_height)

    @app.route("/shopping_list/edit")
    def show_shopping_list_edit_screen() -> str:
        """
        Returns the rendered edit shopping list page.
        """
        locations = controller.get_locations()
        ingredients = controller.get_ingredients()
        recipes = controller.get_recipes()
        return render_template("edit_shopping_list.html",
                               locations=locations,
                               ingredients=ingredients,
                               selected_location=None,
                               recipes=recipes)

    @app.route("/shopping_list/edit/<int:location_id>")
    def show_section_edit_screen(location_id: int) -> str:
        """
        Return the rendered edit shopping list page of a particular location.

        :param location_id: The primary integer key of the location.
        """
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
    def check_recipe(recipe_id: int, week: int, scroll_height: int) -> BaseResponse:
        """
        Select recipe in shopping list for a particular week.

        :param recipe_id: The primary integer key of the recipe.
        :param week: The week number the recipe is added for.
        :param scroll_height: The current scroll height of the page
        :return: The rendered shopping list page with the recipe selected.
        """
        for r in controller.get_recipes():
            if r.id == int(recipe_id):
                r.select(week)
                session["scroll_height"] = scroll_height
                return redirect("/")

    @app.route("/uncheck_recipe/<recipe_id>_<int:week>_<int:scroll_height>")
    def uncheck_recipe(recipe_id: int, week: int, scroll_height: int) -> BaseResponse:
        """
        Unselect recipe in shopping list for a particular week.

        :param recipe_id: The primary integer key of the recipe to uncheck
        :param week: The week number the recipe is unchecked for
        :param scroll_height: The current scroll height of the page
        :return: The rendered shopping list page with the recipe unselected.
        """
        for i in controller.get_recipes():
            if i.id == int(recipe_id):
                i.unselect(week)
                session["scroll_height"] = scroll_height
        return redirect("/")

    @app.route("/reset_recipe_selection")
    def reset_recipe_selection() -> BaseResponse:
        """
        Resets the food plan's current recipe selection.

        :return: Return to main page
        """

        for recipe in controller.get_recipes():
            recipe.selected = False
            recipe.weeks = []
        return redirect("/")

    @app.route("/show_shopping_list", methods=["POST"])
    def show_shopping_list() -> str:
        """
        Display the shopping list page.

        :return: The rendered shopping list page.
        """
        recipes = controller.get_recipes()
        shopping_lists = controller.get_shopping_lists()
        food_plan = FoodPlan(shopping_lists)
        food_plan.set_shopping_lists(recipes)
        controller.food_plan = food_plan
        return render_template("main_screen.html",
                               recipes=recipes,
                               food_plan=food_plan)

    @app.route("/add_recipe")
    def show_add_recipe_screen() -> str:
        """
        Display the screen to add a recipe.

        :return: The rendered add recipe page.
        """
        ingredients = controller.get_ingredients()
        recipes = controller.get_recipes()
        return render_template("add_recipe_screen.html",
                               recipes=recipes,
                               ingredients=ingredients,
                               unit=Unit)

    @app.route("/edit_recipe/<int:recipe_id>")
    def show_edit_recipe_screen(recipe_id) -> str:
        """
        Display the screen to edit a recipe.

        :param recipe_id: The primary integer key of the recipe to edit.
        :return: The rendered edit recipe page.
        """
        recipes = controller.get_recipes()
        recipe = controller.get_recipe(recipe_id)
        recipe_ingredients = controller.get_recipe_ingredients(recipe_id)
        return render_template("edit_recipe_screen.html",
                               recipes=recipes,
                               recipe=recipe,
                               recipe_ingredients=recipe_ingredients,
                               ingredients=controller.get_food_only_ingredients(),
                               unit=Unit
                               )

    @app.route("/print_shopping_list", methods=["POST"])
    def print_shopping_list() -> str:
        """
        Display the printable shopping list page.

        :return: The rendered shopping list page.
        """
        food_plan = controller.food_plan
        return render_template("print_shopping_list.html",
                               food_plan=food_plan)

    @app.route(
        "/confirm_edit_recipe/<int:recipe_id>_<int:amount_ingredients>_"
        "<int:scroll_height>", methods=["POST"])
    def confirm_edit_recipe(recipe_id: int, amount_ingredients: int,
                            scroll_height: int) -> BaseResponse:
        """
        Confirms the current recipe data and close the screen.

        :param recipe_id: The primary integer key of the edited recipe.
        :param amount_ingredients: The amount of ingredients that the recipe has.
        :param scroll_height: The current scroll height on the main page.
        """

        r_name = request.form["recipe_name"]
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

        controller.db.session.expire_on_commit = False
        controller.db.session.commit()
        session["scroll_height"] = scroll_height
        return redirect("/")

    @app.route("/delete_recipe/<int:recipe_id>_<int:scroll_height>")
    def delete_recipe(recipe_id, scroll_height) -> BaseResponse:
        """
        Delete the specified recipe.

        :param recipe_id: The primary integer key of the recipe to delete.
        :param scroll_height: The current scroll height on the main page.
        """
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        recipe.delete()
        session["scroll_height"] = scroll_height
        return redirect("/")

    @app.route(
        "/confirm_new_recipe/<int:amount_ingredients>_<int:scroll_height>",
        methods=["POST"])
    def add_new_recipe(amount_ingredients: int, scroll_height: int) -> BaseResponse:
        """
        Confirm a new recipe and closing the editing screen.

        :param amount_ingredients: The amount of ingredients that the recipe has.
        :param scroll_height: The current scroll height on the main page.
        :return: Navigate back to the main page.
        """
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

        controller.db.session.expire_on_commit = False
        controller.db.session.commit()
        session["scroll_height"] = scroll_height
        return redirect("/")

    @app.route("/ingredients/new")
    def show_add_ingredient_screen() -> str:
        """
        Display the screen to add a new ingredient.
        """
        return render_template("add_ingredient_screen.html",
                               recipes=controller.get_recipes(),
                               ingredients=controller.get_ingredients(),
                               locations=controller.get_locations(),
                               location=None
                               )

    @app.route("/ingredients/edit/<int:ingredient_id>")
    def show_edit_ingredient_screen(ingredient_id: int) -> str:
        """
        Display the screen to edit an existing ingredient.

        :param ingredient_id: The primary integer key of the ingredient to edit.
        """
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
                               ingredients=controller.get_food_only_ingredients(),
                               locations=controller.get_locations(),
                               ingredient=ingredient,
                               location=location,
                               section=section
                               )

    @app.route("/ingredients/delete/<int:ingredient_id>")
    def delete_ingredient(ingredient_id: int) -> BaseResponse:
        """
        Deletes the ingredient which matches the :param:`ingredient_id`.

        :param ingredient_id: THe primary integer key of the ingredient to delete.
        :return: Navigates to the ingredients list page.
        """
        ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        ingredient.delete()
        return redirect("/ingredients")

    @app.route(
        "/confirm_new_ingredient/<int:location_id>_<signed_int"
        ":section_order_id>_<string:non_food>",
        methods=["POST", "GET"])
    def add_ingredient(location_id: int, section_order_id: int, non_food: str) -> BaseResponse:
        """
        Add a new ingredient to the list of ingredients.

        :param location_id: The primary integer key of the location to add.
        :param section_order_id: The primary integer key of the section the ingredient is added to.
        :param non_food: A boolean string ("true"/"false") defining if ingredient is food or not.
        :return: Navigate back to the ingredients list page.
        """

        form = json.loads(str(request.data, "utf-8"))
        name = form["ingredient_name"]
        always_on_list = Helper.bool_string_to_int(form["always_on_list"])
        section_id = controller.get_section_id(location_id,
                                               section_order_id)
        current_max_order_id = controller.get_highest_order_id(Ingredient,
                                                               section_id=section_id)

        i = Ingredient(name=name, always_on_list=always_on_list,
                       location_id=location_id,
                       section_id=section_id,
                       non_food=Helper.bool_string_to_int(non_food),
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
    def confirm_edit_ingredient(ingredient_id: int, location_id: int,
                                section_order_id: int, non_food: str) -> BaseResponse:
        """
        Apply edited changes to ingredient.

        :param ingredient_id: The primary integer key of the edited ingredient.
        :param location_id: The primary integer key of the location of the edited ingredient.
        :param section_order_id: The primary integer key of the section of the edited ingredient.
        :param non_food: A boolean string ("true"/"false") defining if ingredient is food or not.
        :return: Navigate back to the ingredients list page.
        """

        form = json.loads(str(request.data, "utf-8"))
        name = form["ingredient_name"]
        always_on_list = Helper.bool_string_to_int(form["always_on_list"])
        section_id = controller.get_section_id(location_id,
                                               section_order_id)
        existing_ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
        order_id = controller.get_highest_order_id(Ingredient, section_id=section_id)

        try:
            # TODO: add update method to Ingredient model class
            existing_ingredient.name = name
            existing_ingredient.location_id = location_id
            existing_ingredient.order_id = order_id + 1
            existing_ingredient.section_id = section_id
            existing_ingredient.always_on_list = always_on_list
            existing_ingredient.non_food = Helper.bool_string_to_int(non_food)

            controller.db.session.commit()

        except DuplicateIngredientError:
            response = make_response()
            response.status = 409
            response.header = "Duplicate Ingredient Error"
            return response

        return redirect("/ingredients")

    @app.route(
        "/update_ingredient_order/<int:location_id>/<signed_int:section_id>/"
        "<string:new_ingr_id_order>/<int:scroll_height>")
    def set_new_ingredient_order(location_id: int, section_id: int,
                                 new_ingr_id_order: str, scroll_height: int) -> BaseResponse:
        """
        Change the order of the ingredient within the section.

        :param location_id: The primary integer key of the location of the edited ingredient.
        :param section_id: The primary integer key of the section of the edited ingredient.
        :param new_ingr_id_order: The section's ingredients primary keys in their new order.
        :param scroll_height: The current scroll height of the ingredients list page.
        :return: Navigate back to the ingredients list page.
        """
        new_ingr_id_order = new_ingr_id_order.split("_")
        section = Section.query.filter_by(location_id=location_id,
                                          id=section_id).first()
        ingredients = section.get_ingredients()
        current_ingr_id_order = [i.id for i in ingredients]

        for i in range(len(new_ingr_id_order)):
            if new_ingr_id_order[i] == current_ingr_id_order[i]:
                continue
            else:
                Ingredient.query.filter_by(
                    id=new_ingr_id_order[i]).first().update_order_id(i)
        return redirect(f"/shopping_list/{scroll_height}")

    @app.route("/update_location_order/<string:new_loc_id_order>")
    def set_new_location_order(new_loc_id_order: str) -> BaseResponse:
        """
        Change the order of a location on the shopping list.

        :param new_loc_id_order: The location primary keys in their new order.
        """
        new_loc_id_order = new_loc_id_order.split("_")
        locations = controller.get_locations()
        current_loc_id_order = [l.id for l in locations]

        for i in range(len(new_loc_id_order)):
            if new_loc_id_order[i] == current_loc_id_order[i]:
                continue
            else:
                Location.query.filter_by(
                    id=new_loc_id_order[i]).first().update_order_id(i)

        return redirect("/shopping_list/edit")

    @app.route(
        "/update_section_order/<int:location_id>/<string:new_sec_id_order>")
    def set_new_section_order(location_id: int, new_sec_id_order: str) -> BaseResponse:
        """
        Change the order of a section inside a location on the shopping list.

        :param location_id: The location primary key.
        :param new_sec_id_order: The location primary keys in their new order.
        """
        new_sec_id_order = new_sec_id_order.split("_")
        sections = controller.get_sections(location_id)

        current_sec_id_order = [s.id for s in sections]

        for i in range(len(new_sec_id_order)):
            if new_sec_id_order[i] == current_sec_id_order[i]:
                continue
            else:
                Section.query.filter_by(
                    id=new_sec_id_order[i]).first().update_order_id(i)

        return redirect(f"/shopping_list/edit/{location_id}")


    app.run(port=port, debug=True)
