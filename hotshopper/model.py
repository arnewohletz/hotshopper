# Standard library imports
from __future__ import annotations
from dataclasses import dataclass
from typing import Union

# Third-Party library imports
from sqlalchemy import (
    orm,
    Column,
    Integer,
    Float,
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    backref,
    DeclarativeBase,
    relationship
)

# Intra-package imports
from hotshopper.errors import (
    DuplicateIngredientError,
    DuplicateRecipeError,
    DuplicateRecipeIngredientError,
    RecipeIngredientNotFoundError
)


class Base(DeclarativeBase):
    pass


class OrderedModel(Base):
    __abstract__ = True
    id = -1
    order_id = -1


class Ingredient(OrderedModel):
    __tablename__ = "ingredient"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    order_id = Column("order_id", Integer)
    location_id = Column("location_id", Integer)
    recipes = relationship("RecipeIngredient",
                           backref=backref("ingredient", lazy=False),
                           lazy="subquery")
    section_id = Column(Integer, ForeignKey("section.id"))
    always_on_list = Column("always_on_list", Integer)
    non_food = Column("non_food", Integer)
    shopping_list_items = [None, None, None]

    @orm.reconstructor
    def _initialize(self):
        self.shopping_list_items = [None, None, None]

    def update_order_id(self, order_id, session):
        self.order_id = order_id
        session.commit()

    def add(self, session):
        exists = session.query(Ingredient).filter_by(
            name=self.name).first()
        if exists is not None:
            raise DuplicateIngredientError("Ingredient with the same "
                                           "name already exists. Choose "
                                           "different name!")
        else:
            session.add(self)
            session.commit()
            session.flush()    # probably not needed

    def delete(self, session):
        ingredient = session.query(Ingredient).filter_by(id=self.id).first()
        session.delete(ingredient)
        recipe_ingredients = session.query(RecipeIngredient).filter_by(
            ingredient_id=self.id).all()
        for ri in recipe_ingredients:
            session.delete(ri)
        session.commit()

    def update(self):
        raise NotImplementedError

    def used_by(self, session) -> list:
        result = []
        ris = session.query(RecipeIngredient).filter_by(
            ingredient_id=self.id).all()
        for ri in ris:
            r = session.query(Recipe).filter_by(id=ri.recipe_id).first()
            result.append(r.name)

        return result

    def must_be_on_list(self):
        if self.always_on_list:
            return True

    def has_shopping_list_item(self, week_index):
        return self.shopping_list_items[week_index] is not None


class Location(OrderedModel):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    order_id = Column(String)
    sections = relationship("Section", backref="location",
                            order_by="asc(Section.order_id)")
    shopping_lists = relationship("ShoppingList",
                                  secondary="shopping_list_location",
                                  back_populates="locations")

    def __init__(self, session, name, order_id, **kw):
        super().__init__(**kw)
        self.name = name
        self.order_id = order_id
        self.existing_sections = session.query(Section).filter_by(
            location_id=self.id).all()
        self.sections = []
        for section in self.existing_sections:
            self.sections.append(section)
            # self.sections.append(Section(session, section.id, section.name,
            #                              section.order_id))

    def update_order_id(self, order_id, session):
        self.order_id = order_id
        session.commit()

    def has_shopping_list_items(self, week_index):
        for section in self.sections:
            if section.has_shopping_list_items(week_index):
                return True
        return False


class Recipe(Base):
    __tablename__ = "recipe"
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = relationship("RecipeIngredient",
                               backref=backref("recipe", lazy=False),
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
        print(f"{self.name} is selected for week {str(week)}")

    def unselect(self, week: int):
        self.weeks.remove(week)
        if len(self.weeks) == 0:
            self.selected = False
            self.weeks = []
        print(f"{self.name} is deselected from week {str(week)}")

    def add_ingredient(self, ingredient: RecipeIngredient, session):
        existing = session.query(RecipeIngredient).filter_by(
            recipe_id=self.id,
            ingredient_id=ingredient.ingredient_id).all()
        if existing:
            raise DuplicateRecipeIngredientError(
                "Ingredient already exists for this recipe. Won't add")
        session.add(ingredient)
        session.commit()

    def delete(self, session):
        recipe = session.query(Recipe).filter_by(id=self.id).first()
        recipe_ingredients = session.query(RecipeIngredient).filter_by(
            recipe_id=recipe.id).all()
        session.delete(recipe)
        for ri in recipe_ingredients:
            session.delete(ri)
        session.commit()

    def add(self, session):
        exists = session.query(Recipe).filter_by(name=self.name).first()
        if exists:
            raise DuplicateRecipeError("Recipe with same name already exists")
        else:
            session.add(self)
            session.flush()
            return self.id

    def update(self, session, name: str = None):
        self.name = name
        session.commit()

    @staticmethod
    def save_recipe(session):
        session.commit()


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"
    recipe_id = Column(ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = Column(ForeignKey("ingredient.id"), primary_key=True)
    quantity_per_person = Column(Float)
    unit = Column(String)
    amount_piece = 0
    amount = 0

    def update(self, session, quantity_per_person: Union[float, int] = None,
               unit: str = None,
               ingredient_id: int = None):
        if quantity_per_person is not None:
            if (not isinstance(quantity_per_person, (int, float))
                    or not 1.0 <= quantity_per_person <= 10000):
                raise ValueError("Enter value between 1.0 and 10000.0")
            self.quantity_per_person = quantity_per_person
        if ingredient_id is not None:
            self.ingredient_id = ingredient_id
        if unit:
            self.unit = unit

        session.commit()

    def add(self, session):
        exists = session.query(RecipeIngredient).filter_by(
            ingredient_id=self.ingredient_id,
            recipe_id=self.recipe_id).first()
        if exists:
            raise DuplicateRecipeIngredientError("Recipe already uses "
                                                 "ingredient with same name")
        else:
            session.add(self)
            session.flush()

    def delete(self, session):
        ingredient = session.query(RecipeIngredient).filter_by(
            ingredient_id=self.ingredient_id,
            recipe_id=self.recipe_id).first()
        if ingredient:
            session.delete(ingredient)
            session.commit()
            return True
        raise RecipeIngredientNotFoundError(
            f"Can't delete ingredient {ingredient.name}, "
            f"as it is not found in recipe")


class Section(Base):
    __tablename__ = "section"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    order_id = Column(Integer)
    location_id = Column(Integer, ForeignKey("location.id"))
    ingredients = relationship("Ingredient", backref="section")

    def __init__(self, name, order_id, **kw):
        super().__init__(**kw)
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

    def update_order_id(self, order_id, session):
        self.order_id = order_id
        session.commit()


class ShoppingList(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    weeks = relationship("Week",
                         secondary="shopping_list_week",
                         back_populates="shopping_lists")
    locations = relationship("Location",
                             secondary="shopping_list_location",
                             back_populates="shopping_lists",
                             order_by="asc(Location.order_id)")
    ingredients = None
    print_columns = Column(Integer)

    @orm.reconstructor  # called after object was loaded from database
    def initialize(self):
        self.ingredients = []

    def __contains__(self, class_type):
        for ingredient in self.ingredients:
            if isinstance(ingredient, class_type):
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
        list_item = ShoppingListItem(recipe_ingredient)

        for location in self.locations:
            for section in location.sections:
                for ingredient in section.ingredients:
                    if ingredient.id == recipe_ingredient.ingredient_id:
                        week_index = self.weeks[0].number - 1
                        if ingredient.has_shopping_list_item(
                                week_index=week_index):
                            ingredient.shopping_list_items[
                                week_index] += list_item
                        else:
                            ingredient.shopping_list_items[
                                week_index] = list_item
                        return True
        raise KeyError(f"Cannot find ingredient entry for "
                       f"'{recipe_ingredient.ingredient.name}'")

    def sort_ingredients(self):
        self.ingredients.sort(key=lambda ri: ri.order_id)


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

    def __add__(self, other):
        if self.name is not other.name:
            raise ValueError(f"Name mismatch: Can't add '{other.name}'"
                             f"to {self.name}")
        if self.order_id is not other.order_id:
            raise ValueError(f"Order ID mismatch: Existing item has order id "
                             f"{self.order_id}, but added item "
                             f"uses {other.order_id}")
        self.amount += other.amount
        self.amount_piece += other.amount_piece
        return self

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


class ShoppingListLocation(Base):
    __tablename__ = "shopping_list_location"
    shopping_list_id = Column(Integer,
                              ForeignKey("shopping_list.id"),
                              primary_key=True)
    location_id = Column(Integer,
                         ForeignKey("location.id"),
                         primary_key=True)


class ShoppingListWeek(Base):
    __tablename__ = "shopping_list_week"
    shopping_list_id = Column(Integer,
                              ForeignKey("shopping_list.id"),
                              primary_key=True)
    week_id = Column(Integer,
                     ForeignKey("week.id"),
                     primary_key=True)


@dataclass
class Unit:
    GRAM: str = "g"
    PIECE: str = "St."


class Week(Base):
    __tablename__ = "week"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    shopping_lists = relationship("ShoppingList",
                                  secondary="shopping_list_week",
                                  back_populates="weeks")
