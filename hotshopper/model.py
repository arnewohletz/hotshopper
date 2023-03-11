from typing import Union, NewType
from sqlalchemy import orm
import copy

from hotshopper import db
from hotshopper.constants import Unit
from hotshopper.errors import (DuplicateIngredientError,
                               DuplicateRecipeError,
                               DuplicateRecipeIngredientError,
                               RecipeIngredientNotFoundError)

# used for type hints only
RecipeIngredient = NewType("RecipeIngredient", None)


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    order_id = db.Column("order_id", db.Integer)
    location_id = db.Column("location_id", db.Integer)
    recipes = db.relationship("RecipeIngredient",
                              backref=db.backref("ingredient", lazy=False),
                              lazy="subquery")
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    always_on_list = db.Column("always_on_list", db.Integer)
    non_food = db.Column("non_food", db.Integer)
    shopping_list_item = None

    def update_order_id(self, order_id):
        self.order_id = order_id
        db.session.commit()
        # db.session.add(self)
        # db.session.flush()

    def add(self):
        exists = Ingredient.query.filter_by(
            name=self.name).first()
        if exists:
            raise DuplicateIngredientError("Ingredient with the same "
                                           "name already exists. Choose "
                                           "different name!")
        else:
            db.session.add(self)
            db.session.commit()

    def delete(self):
        ingredient = Ingredient.query.filter_by(id=self.id).first()
        db.session.delete(ingredient)
        recipe_ingredients = RecipeIngredient.query.filter_by(
            ingredient_id=self.id).all()
        for ri in recipe_ingredients:
            db.session.delete(ri)
        db.session.commit()


    def used_by(self) -> list:
        result = []
        ris = RecipeIngredient.query.filter_by(ingredient_id=self.id).all()
        for ri in ris:
            r = Recipe.query.filter_by(id=ri.recipe_id).first()
            result.append(r.name)

        return result

    def has_shopping_list_item(self):
        return self.shopping_list_item is not None


class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship("RecipeIngredient",
                                  backref=db.backref("recipe", lazy=False),
                                  lazy="joined")
    weeks: list = None
    selected = False

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def select(self, week: int):
        if not self.weeks:
            self.weeks = []
        self.selected = True
        self.weeks.append(week)
        print(self.name + " is selected for week " + str(week))

    def unselect(self, week: int):
        self.weeks.remove(week)
        if len(self.weeks) == 0:
            self.selected = False
            self.weeks = []
        print(self.name + " is deselected from week " + str(week))

    def add_ingredient(self, ingredient: RecipeIngredient):
        existing = RecipeIngredient.query.filter_by(recipe_id=self.id,
                                                    ingredient_id=ingredient.ingredient_id).all()
        if existing:
            raise DuplicateRecipeIngredientError(
                "Ingredient already exists for this recipe. Won't add")
        db.session.add(ingredient)
        db.session.commit()

    def delete(self):
        recipe = Recipe.query.filter_by(id=self.id).first()
        recipe_ingredients = RecipeIngredient.query.filter_by(
            recipe_id=recipe.id).all()
        db.session.delete(recipe)
        for ri in recipe_ingredients:
            db.session.delete(ri)
        db.session.commit()

    def add(self):
        exists = Recipe.query.filter_by(name=self.name).first()
        if exists:
            raise DuplicateRecipeError("Recipe with same name already exists")
        else:
            db.session.add(self)
            db.session.flush()
            return self.id

    def update(self, name: str = None):
        self.name = name
        db.session.commit()

    @staticmethod
    def save_recipe():
        db.session.commit()


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"
    recipe_id = db.Column(db.ForeignKey("recipe.id"),
                          primary_key=True)
    ingredient_id = db.Column(db.ForeignKey("ingredient.id"),
                              primary_key=True)
    quantity_per_person = db.Column(db.Integer)
    unit = db.Column(db.String)
    amount_piece = 0
    amount = 0

    # @orm.reconstructor  # called after object was loaded from database
    # def assign_amount(self):
    #     """
    #     Maps per person quantity to total quantity
    #     :return: None
    #     """
    #     if self.unit == "st.":
    #         self.amount = 0
    #         self.amount_piece = self.quantity_per_person
    #     else:
    #         self.amount_piece = 0
    #         self.amount = self.quantity_per_person

    def update(self, quantity_per_person: Union[float, int] = None,
               unit: str = None,
               ingredient_id: int = None):
        if quantity_per_person is not None:
            if not isinstance(quantity_per_person, (int, float)) \
                or not 1.0 <= quantity_per_person <= 10000:
                raise ValueError("Enter value between 1.0 and 10000.0")
            self.quantity_per_person = quantity_per_person
        if ingredient_id is not None:
            self.ingredient_id = ingredient_id
        if unit:
            self.unit = unit

        db.session.commit()

    def add(self):
        exists = RecipeIngredient.query.filter_by(
            ingredient_id=self.ingredient_id,
            recipe_id=self.recipe_id).first()
        if exists:
            raise DuplicateRecipeIngredientError("Recipe already uses "
                                                 "ingredient with same name")
        else:
            db.session.add(self)
            db.session.flush()

    def delete(self):
        ingredient = RecipeIngredient.query.filter_by(
            ingredient_id=self.ingredient_id, recipe_id=self.recipe_id).first()
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return True
        raise RecipeIngredientNotFoundError(
            f"Can't delete ingredient, as it"
            f" is not found in recipe")


class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    order_id = db.Column(db.String)
    sections = db.relationship("Section", backref="location")
    shopping_lists = db.relationship("ShoppingList",
                                     secondary="shopping_list_location",
                                     back_populates="locations")
    # ingredients = db.relationship("Ingredient", backref="locationIngredients")
    # non_food_items = db.relationship("NonFoodItem", backref="locationNonFood")

    def update_order_id(self, order_id):
        self.order_id = order_id
        db.session.commit()


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    order_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    ingredients = db.relationship("Ingredient", backref="section")

    # non_food_items = db.relationship("NonFoodItem", backref="sectionNonFood")

    def get_ingredients(self):
        return sorted(self.ingredients,
                      key=lambda ingredient: ingredient.order_id)

    # def add(self, ingredient):
    #     # TODO: ShoppingListIngredient must be put into shopping_list > location > section
    #     if ingredient.unit == Unit.PIECE:
    #         ingredient.amount_piece = ingredient.quantity_per_person
    #     else:
    #         ingredient.amount = ingredient.quantity_per_person
    #
    #     for existing_ingredient in self.ingredients:
    #         if ingredient.ingredient.name == existing_ingredient.name:
    #             if ingredient.unit == Unit.PIECE:
    #                 # TODO: Add multiplied by 'persons' once added to recipe
    #                 existing_ingredient.amount_piece += ingredient.amount_piece
    #             else:
    #                 existing_ingredient.amount += ingredient.amount
    #             return True
    #     # self.ingredients.append(ShoppingListIngredient(ingredient))
    #     # Copy required since shopping list otherwise alters the ingredient
    #     # amount in the recipe, when adding them (not nice, I know)
    #     self.ingredients.append(ShoppingListItem(copy.deepcopy(ingredient)))


class ShoppingListLocation(db.Model):
    __tablename__ = "shopping_list_location"
    shopping_list_id = db.Column(db.Integer, db.ForeignKey("shopping_list.id"), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), primary_key=True)


class ShoppingListWeek(db.Model):
    __tablename__ = "shopping_list_week"
    shopping_list_id = db.Column(db.Integer, db.ForeignKey("shopping_list.id"), primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), primary_key=True)


class Week(db.Model):
    __tablename__ = "week"
    id = db.Column(db.Integer, primary_key=True)
    shopping_lists = db.relationship("ShoppingList",
                                     secondary="shopping_list_week",
                                     back_populates="weeks")

class ShoppingList(db.Model):
    __tablename__ = "shopping_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    weeks = db.relationship("Week", secondary="shopping_list_week",
                            back_populates="shopping_lists")
                            # backref=db.backref("shopping_lists"))
    # locations = db.relationship("Location", secondary="shopping_list_location",
    #                             backref=db.backref("shopping_list_id", lazy=False),
    #                             lazy="joined")
    locations = db.relationship("Location", secondary="shopping_list_location",
                            back_populates="shopping_lists")

    ingredients = None
    @orm.reconstructor  # called after object was loaded from database
    def initialize(self):
        self.ingredients = []
    # ingredients = db.relationship("RecipeIngredient",
    #                               backref=db.backref("recipe", lazy=False),
    #                               lazy="joined")

    # def __init__(self, name, locations, weeks):
    #     super().__init__()
    #     self.name = name
    #     self.locations = locations
    #     self.weeks = weeks

    def __contains__(self, type):
        for ingredient in self.ingredients:
            if isinstance(ingredient, type):
                return True
            return False

    def has_location(self, location_id):
        for loc in self.locations:
            if location_id == loc.id:
                return True
        return False

    def has_week(self, week):
        return week in [week.id for week in self.weeks]
        # matches = set(week.id for week in self.weeks).intersection(set(*weeks))
        # if len(matches) > 0:
        #     return True
        # else:
        #     return False

    def get_name(self):
        return self.name

    def add(self, recipe_ingredient: RecipeIngredient):
        matching_ingredient = None
        list_item = ShoppingListItem(recipe_ingredient)

        for location in self.locations:
            for section in location.sections:
                for ingredient in section.ingredients:
                    if ingredient.id == recipe_ingredient.ingredient_id:
                        matching_ingredient = ingredient

        if matching_ingredient.has_shopping_list_item():
            matching_ingredient.shopping_list_item += list_item
        else:
            matching_ingredient.shopping_list_item = list_item
        return True
        #
        # ingredient = Ingredient.query.filter_by(id=recipe_ingredient.ingredient_id)
        # ingredient = Ingredient.query.filter_by(id=recipe_ingredient.ingredient.location_id).first()
        #
        # if not self.list_item:
        #     self.list_item = ShoppingListItem(recipe_ingredient)
        #
        # if self.list_item.unit == Unit.PIECE:
        #     recipe_ingredient.amount_piece = recipe_ingredient.quantity_per_person
        # else:
        #     recipe_ingredient.amount = recipe_ingredient.quantity_per_person
        #
        #
        # for location in self.locations:
        #     if location.ingredients:
        #         location.add_ingredient(recipe_ingredient)
        #         for existing_ing in location.ingredients:
        #             if existing_ing.id == recipe_ingredient.ingredient_id:
        #                 existing_ing.amount_piece += recipe_ingredient.amount_piece
        #                 existing_ing.amount += recipe_ingredient.amount
        #                 return True
        #     if location.sections:
        #         for section in location.sections:
        #             for existing_ing in section.ingredients:
        #                 if existing_ing.id == recipe_ingredient.ingredient_id:
        #                     existing_ing.amount_piece += recipe_ingredient.amount_piece
        #                     existing_ing.amount += recipe_ingredient.amount
        #                     return True
        #             if section.id == recipe_ingredient.section_id:
        #                 raise NotImplementedError
        #
        # for existing_ingredient in self.ingredients:
        #     if recipe_ingredient.ingredient.name == existing_ingredient.name:
        #         if recipe_ingredient.unit == Unit.PIECE:
        #             # TODO: Add multiplied by 'persons' once added to recipe
        #             # TODO: Add "ShoppingListItem" to Ingredient instance of ShoppingList
        #             existing_ingredient.amount_piece += recipe_ingredient.amount_piece
        #             recipe_ingredient.ingredient.shopping_list_item.amount_piece += recipe_ingredient.amount_piece
        #         else:
        #             existing_ingredient.amount += recipe_ingredient.amount
        #             recipe_ingredient.ingredient.shopping_list_item.amount += existing_ingredient.amount
        #         return True
        # # self.ingredients.append(ShoppingListIngredient(ingredient))
        # # Copy required since shopping list otherwise alters the ingredient
        # # amount in the recipe, when adding them (not nice, I know)
        # self.ingredients.append(ShoppingListItem(copy.deepcopy(recipe_ingredient)))
    #
    def sort_ingredients(self):
        self.ingredients.sort(key=lambda ri: ri.order_id)
    #
    def append_always_on_list_items(self):
        # TODO: Implement append_always_on_list_items() method
        raise NotImplementedError


class ShoppingListItem:
    """
    Stripped down, non-database model representation of
    :class:`RecipeIngredient` to be added to :class:`ShoppingList`.
    """

    def __init__(self, recipe_ingredient: RecipeIngredient):
        self.amount_piece = self.amount = 0
        if recipe_ingredient.unit == Unit.GRAM:
            self.amount = recipe_ingredient.quantity_per_person
        if recipe_ingredient.unit == Unit.PIECE:
            self.amount_piece = recipe_ingredient.quantity_per_person
        self.name = recipe_ingredient.ingredient.name
        self.order_id = recipe_ingredient.ingredient.order_id
        self.unit = recipe_ingredient.unit
        # self.amount = recipe_ingredient.amount
        # self.amount_piece = recipe_ingredient.amount_piece

    def __add__(self, other):
        if self.name is not other.name:
            raise ValueError(f"Name mismatch: Can't add '{other.name}' to {self.name}")
        if self.order_id is not other.order_id:
            raise ValueError(f"Order ID mismatch: Existing item has order id "
                             f"{self.order_id}, but addend uses {other.order_id}")
        self.amount += other.amount
        self.amount_piece += other.amount_piece
        # TODO: I am caring about the unit here. Might be an issue...

    def print_amounts(self):
        # TODO: Should return both amount_piece and amount, if both > 0
        result = ""
        if self.amount_piece > 0:
            if float(self.amount_piece).is_integer():
                self.amount_piece = int(self.amount_piece)
            result = f"{self.amount_piece} St."
            if self.amount > 0:
                result += " + "
        if self.amount > 0:
            if float(self.amount).is_integer():
                self.amount = int(self.amount)
            result += f"{self.amount} g"
        return result
