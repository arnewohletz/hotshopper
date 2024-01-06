from dataclasses import dataclass
from typing import Union, NewType
from sqlalchemy import orm

from hotshopper import _db
from hotshopper.constants import Unit
from hotshopper.errors import (DuplicateIngredientError,
                               DuplicateRecipeError,
                               DuplicateRecipeIngredientError,
                               RecipeIngredientNotFoundError)

# used as type hint only
RecipeIngredient = NewType("RecipeIngredient", None)

@dataclass
class Ingredient(_db.Model):
    __tablename__ = "ingredient"
    id = _db.Column("id", _db.Integer, primary_key=True)
    name = _db.Column("name", _db.String)
    order_id = _db.Column("order_id", _db.Integer)
    location_id = _db.Column("location_id", _db.Integer)
    recipes = _db.relationship("RecipeIngredient",
                               backref=_db.backref("ingredient", lazy=False),
                               lazy="subquery")
    section_id = _db.Column(_db.Integer, _db.ForeignKey("section.id"))
    always_on_list = _db.Column("always_on_list", _db.Integer)
    non_food = _db.Column("non_food", _db.Integer)
    shopping_list_item = None

    @orm.reconstructor
    def _initialize(self):
        self.shopping_list_item = [None, None, None]

    def update_order_id(self, order_id):
        self.order_id = order_id
        _db.session.commit()

    def add(self):
        exists = Ingredient.query.filter_by(
            name=self.name).first()
        if exists is not None:
            raise DuplicateIngredientError("Ingredient with the same "
                                           "name already exists. Choose "
                                           "different name!")
        else:
            _db.session.add(self)
            _db.session.commit()
            _db.session.flush()    # probably not needed

    def delete(self):
        ingredient = Ingredient.query.filter_by(id=self.id).first()
        _db.session.delete(ingredient)
        recipe_ingredients = RecipeIngredient.query.filter_by(
            ingredient_id=self.id).all()
        for ri in recipe_ingredients:
            _db.session.delete(ri)
        _db.session.commit()

    def update(self):
        raise NotImplementedError

    def used_by(self) -> list:
        result = []
        ris = RecipeIngredient.query.filter_by(ingredient_id=self.id).all()
        for ri in ris:
            r = Recipe.query.filter_by(id=ri.recipe_id).first()
            result.append(r.name)

        return result

    def must_be_on_list(self):
        if self.always_on_list:
            return True

    def has_shopping_list_item(self, week_index):
        return self.shopping_list_item[week_index] is not None

@dataclass
class Recipe(_db.Model):
    __tablename__ = "recipe"
    __allow_unmapped__ = True
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String)
    ingredients = _db.relationship("RecipeIngredient",
                                   backref=_db.backref("recipe", lazy=False),
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
        _db.session.add(ingredient)
        _db.session.commit()

    def delete(self):
        recipe = Recipe.query.filter_by(id=self.id).first()
        recipe_ingredients = RecipeIngredient.query.filter_by(
            recipe_id=recipe.id).all()
        _db.session.delete(recipe)
        for ri in recipe_ingredients:
            _db.session.delete(ri)
        _db.session.commit()

    def add(self):
        exists = Recipe.query.filter_by(name=self.name).first()
        if exists:
            raise DuplicateRecipeError("Recipe with same name already exists")
        else:
            _db.session.add(self)
            _db.session.flush()
            return self.id

    def update(self, name: str = None):
        self.name = name
        _db.session.commit()

    @staticmethod
    def save_recipe():
        _db.session.commit()

@dataclass
class RecipeIngredient(_db.Model):
    __tablename__ = "recipe_ingredient"
    recipe_id = _db.Column(_db.ForeignKey("recipe.id"),
                           primary_key=True)
    ingredient_id = _db.Column(_db.ForeignKey("ingredient.id"),
                               primary_key=True)
    quantity_per_person = _db.Column(_db.Integer)
    unit = _db.Column(_db.String)
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

        _db.session.commit()

    def add(self):
        exists = RecipeIngredient.query.filter_by(
            ingredient_id=self.ingredient_id,
            recipe_id=self.recipe_id).first()
        if exists:
            raise DuplicateRecipeIngredientError("Recipe already uses "
                                                 "ingredient with same name")
        else:
            _db.session.add(self)
            _db.session.flush()

    def delete(self):
        ingredient = RecipeIngredient.query.filter_by(
            ingredient_id=self.ingredient_id, recipe_id=self.recipe_id).first()
        if ingredient:
            _db.session.delete(ingredient)
            _db.session.commit()
            return True
        raise RecipeIngredientNotFoundError(
            f"Can't delete ingredient, as it"
            f" is not found in recipe")

@dataclass
class Location(_db.Model):
    __tablename__ = "location"
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String)
    order_id = _db.Column(_db.String)
    sections = _db.relationship("Section", backref="location")
    shopping_lists = _db.relationship("ShoppingList",
                                     secondary="shopping_list_location",
                                     back_populates="locations")

    def __init__(self, name, order_id):
        self.name = name
        self.order_id = order_id
        self.existing_sections = Section.query.filter_by(location_id=self.id).all()
        self.sections = []
        for section in self.existing_sections:
            self.sections.append(Section(section.name, section.order_id))

    def update_order_id(self, order_id):
        self.order_id = order_id
        _db.session.commit()

    def has_shopping_list_items(self, week_index):
        for section in self.sections:
            if section.has_shopping_list_items(week_index):
                return True
        return False

@dataclass
class Section(_db.Model):
    __tablename__ = "section"
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String)
    order_id = _db.Column(_db.Integer)
    location_id = _db.Column(_db.Integer, _db.ForeignKey("location.id"))
    ingredients = _db.relationship("Ingredient", backref="section")

    def __init__(self, name, order_id):
        self.name = name
        self.order_id = order_id

    def get_ingredients(self):
        return sorted(self.ingredients,
                      key=lambda ingredient: ingredient.order_id)

    def has_shopping_list_items(self, week_index):
        for ingredient in self.ingredients:
            if ingredient.must_be_on_list():
                return True
            if ingredient.has_shopping_list_item(week_index):
                return True
        return False


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

@dataclass
class ShoppingListLocation(_db.Model):
    __tablename__ = "shopping_list_location"
    shopping_list_id = _db.Column(_db.Integer, _db.ForeignKey("shopping_list.id"), primary_key=True)
    location_id = _db.Column(_db.Integer, _db.ForeignKey("location.id"), primary_key=True)

@dataclass
class ShoppingListWeek(_db.Model):
    __tablename__ = "shopping_list_week"
    shopping_list_id = _db.Column(_db.Integer, _db.ForeignKey("shopping_list.id"), primary_key=True)
    week_id = _db.Column(_db.Integer, _db.ForeignKey("week.id"), primary_key=True)

@dataclass
class Week(_db.Model):
    __tablename__ = "week"
    id = _db.Column(_db.Integer, primary_key=True)
    number = _db.Column(_db.Integer)
    shopping_lists = _db.relationship("ShoppingList",
                                     secondary="shopping_list_week",
                                     back_populates="weeks")

class ShoppingList(_db.Model):
    __tablename__ = "shopping_list"
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String)
    weeks = _db.relationship("Week", secondary="shopping_list_week",
                            back_populates="shopping_lists")
    # locations = None
                            # backref=db.backref("shopping_lists"))
    # locations = db.relationship("Location", secondary="shopping_list_location",
    #                             backref=db.backref("shopping_list_id", lazy=False),
    #                             lazy="joined")
    # locations_association = db.relationship("Location", secondary="shopping_list_location",
    #                         back_populates="shopping_lists")
    locations = _db.relationship("Location", secondary="shopping_list_location",
                            back_populates="shopping_lists")
    # locations = db.relationship("Location", secondary="shopping_list_location")
    ingredients = None
    # locations = []
    print_columns = _db.Column(_db.Integer)
    # locations = association_proxy('locations_association', 'name')

    # def __init__(self, name: str, locations: list, weeks: list,
    #              print_columns: int):
    #     self.ingredients = None
    #     self.name = name
    #     self.locations = locations
    #     self.weeks = weeks
    #     self.print_columns = print_columns
        # self.existing_locations = db.session.query(Location).all()
        # self.locations = db.relationship("Location", secondary="shopping_list_location",
        #                     back_populates="shopping_lists")
        # for location in self.existing_locations:
        #     self.locations.append(copy.copy(Location(location.name, location.order_id)))

    a = None     # TODO: changing this value does only affect one shopping list instance
                 #  but changing 'locations' does affect all - why?
    # print_columns_width = db.Column(db.Integer)

    # TODO: Add print options:
    #   - Columns total
    #   - Columns width
    #   Rule:
    #   1/2 Columns total <= Columns width <= Columns total


    @orm.reconstructor  # called after object was loaded from database
    def initialize(self):
        self.ingredients = []
        # self.locations = copy.deepcopy(self.locations)
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
        return week in [week.number for week in self.weeks]

    def get_name(self):
        return self.name

    def add(self, recipe_ingredient: RecipeIngredient):
        matching_ingredient = None
        list_item = ShoppingListItem(recipe_ingredient)

        for location in self.locations:
            for section in location.sections:
                for ingredient in section.ingredients:
                    if ingredient.id == recipe_ingredient.ingredient_id:
                        week_index = self.weeks[0].number - 1
                        # if ingredient.must_be_on_list():
                        #     ingredient.shopping_list_item[week_index] = list_item
                            # TODO: Add a week_x attribute to ingredient, one for each entry in self.weeks
                        if ingredient.has_shopping_list_item(week_index=week_index):
                            #
                            # if ingredient.shopping_list_item[self.weeks[0]-1]:
                            ingredient.shopping_list_item[week_index] += list_item
                        else:
                            ingredient.shopping_list_item[week_index] = list_item
                        # else:
                        #     ingredient.shopping_list_item[self.weeks[0]-1] = list_item
                            self.a = ShoppingListItem(recipe_ingredient)
                        return True
        # self.ingredients.append(
        #     ShoppingListItem(copy.deepcopy(recipe_ingredient)))
        raise KeyError(f"Cannot find ingredient entry for {recipe_ingredient.ingredient.name}")
        # if matching_ingredient.has_shopping_list_item():
        #     matching_ingredient.shopping_list_item += list_item
        # else:
        #     matching_ingredient.shopping_list_item = list_item
        # return True
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

@dataclass
class ShoppingListItem:
    """
    Stripped down, non-database model representation of
    :class:`RecipeIngredient` to be added to :class:`ShoppingList`.
    """

    def __init__(self, recipe_ingredient: RecipeIngredient):
        self.ingredient_id = recipe_ingredient.ingredient_id
        self.section_id = recipe_ingredient.ingredient.section_id
        self.location_id = recipe_ingredient.ingredient.location_id
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
        return self
        # TODO: I am caring about the unit here. Might be an issue...

    def print_amounts(self):
        """Prints the amount per gram or/and per piece"""
        result = ""
        if self._is_whole_amount(self.amount_piece):
            self.amount_piece = int(self.amount_piece)
        if self._is_whole_amount(self.amount):
            self.amount = int(self.amount)

        if self.amount_piece > 0:
            result = f"{self.amount_piece} St."
            if self.amount > 0:
                result += f" + {self.amount} g"

        if self.amount > 0:
            result = f"{self.amount} g"
            if self.amount_piece > 0:
                result += f" + {self.amount_piece} St."

        if result == "":
            return "__"
        else:
            return result

    @staticmethod
    def _is_whole_amount(amount):
        return int(amount % 1) == 0
