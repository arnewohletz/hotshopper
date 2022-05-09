from sqlalchemy import orm

from hotshopper import db
from hotshopper.errors import (DuplicateRecipeError,
                               DuplicateRecipeIngredientError,
                               RecipeIngredientNotFoundError)


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

    @orm.reconstructor  # called after object was loaded from database
    def assign_amount(self):
        """
        Maps per person quantity to total quantity
        :return: None
        """
        if self.unit == "st.":
            self.amount = 0
            self.amount_piece = self.quantity_per_person
        else:
            self.amount_piece = 0
            self.amount = self.quantity_per_person

    def update_quantity(self, quantity_per_person: int = None,
                        unit: str = None):
        if quantity_per_person is not None:
            if not isinstance(quantity_per_person, int):
                raise ValueError("Enter positive integer value")
            if not 1 <= quantity_per_person <= 999999:
                raise ValueError("Enter value between 1 and 999999")
            self.quantity_per_person = quantity_per_person
        if unit:
            self.unit = unit

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
            ingredient_id=self.ingredient_id).first()
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return True
        raise RecipeIngredientNotFoundError(
            f"Can't delete ingredient, as it"
            f" is not found in recipe")


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    order_id = db.Column("order_id", db.Integer)
    where = db.Column("where", db.String)
    recipes = db.relationship("RecipeIngredient",
                              backref="ingredient")


class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship("RecipeIngredient",
                                  backref="recipe")
    weeks = None
    selected = False

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

    # def remove_ingredient(self, recipe_ingredient: RecipeIngredient):
    #     ingredient = RecipeIngredient.query.filter_by(
    #         ingredient_id=recipe_ingredient.ingredient_id).first()
    #
    #     if ingredient:
    #         db.session.delete(ingredient)
    #         return True
    #     raise RecipeIngredientNotFoundError(f"Can't delete ingredient, as it"
    #                                         f" is not found in {self.name}")

    def delete(self):
        recipe = Recipe.query.filter_by(id=self.id).first()
        db.session.delete(recipe)
        db.session.commit()

    def add(self):
        exists = Recipe.query.filter_by(name=self.name).first()
        if exists:
            raise DuplicateRecipeError("Recipe with same name already exists")
        else:
            db.session.add(self)
            db.session.flush()
            return self.id

    @staticmethod
    def save_recipe():
        db.session.commit()

    # @staticmethod
    # def cancel_recipe_changes():
    #     db.session.rollback()


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
