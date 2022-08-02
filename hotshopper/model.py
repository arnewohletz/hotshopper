from sqlalchemy import update
from typing import Union, NewType

from hotshopper import db
from hotshopper.errors import (DuplicateRecipeError,
                               DuplicateRecipeIngredientError,
                               RecipeIngredientNotFoundError)

# used for type hints only
RecipeIngredient = NewType("RecipeIngredient", None)


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    order_id = db.Column("order_id", db.Integer)
    where = db.Column("where", db.String)
    recipes = db.relationship("RecipeIngredient",
                              backref=db.backref("ingredient", lazy=False),
                              lazy="subquery")
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    always_on_list = db.Column("always_on_list", db.Integer)
    non_food = db.Column("non_food", db.Integer)

    def update_order_id(self, order_id):
        self.order_id = order_id
        # db.session.commit()
        # db.session.add(self)
        # db.session.flush()


# class NonFoodItem(db.Model):
#     __tablename__ = "nonfood_item"
#     id = db.Column("id", db.Integer, primary_key=True)
#     name = db.Column("name", db.String)
#     order_id = db.Column("order_id", db.Integer)
#     where = db.Column("where", db.String)
#     always_on_list = db.Column("always_on_list", db.Integer)
#     section = db.Column(db.Integer, db.ForeignKey("section.id"))
#     location = db.Column(db.Integer, db.ForeignKey("location.id"))


class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship("RecipeIngredient",
                                  backref=db.backref("recipe", lazy=False),
                                  lazy="joined")
    weeks = None
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
            self.weeks = None
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
    # ingredients = db.relationship("Ingredient", backref="locationIngredients")
    # non_food_items = db.relationship("NonFoodItem", backref="locationNonFood")


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


class ShoppingListIngredient:
    """
    Stripped down, non-database model representation of
    :class:`RecipeIngredient` to be added to :class:`ShoppingList`.
    """

    def __init__(self, recipe_ingredient: RecipeIngredient):
        self.name = recipe_ingredient.ingredient.name
        self.order_id = recipe_ingredient.ingredient.order_id
        self.unit = recipe_ingredient.unit
        self.amount = recipe_ingredient.amount
        self.amount_piece = recipe_ingredient.amount_piece

    def get_amount(self):
        if self.amount_piece > 0:
            if float(self.amount_piece).is_integer():
                return int(self.amount_piece)
            else:
                return self.amount_piece
        elif self.amount > 0:
            if float(self.amount).is_integer():
                return int(self.amount)
            else:
                return self.amount
        else:
            return 0
