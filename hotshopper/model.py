from sqlalchemy import orm

from hotshopper import db


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

    @orm.reconstructor
    def assign_amount(self):
        if self.unit == "st.":
            self.amount = 0
            self.amount_piece = self.quantity_per_person
        else:
            self.amount_piece = 0
            self.amount = self.quantity_per_person

    # def get_amount(self):
    #     if self.amount_piece > 0:
    #         if float(self.amount_piece).is_integer():
    #             return int(self.amount_piece)
    #         else:
    #             return self.amount_piece
    #     elif self.amount > 0:
    #         if float(self.amount).is_integer():
    #             return int(self.amount)
    #         else:
    #             return self.amount
    #     else:
    #         return 0


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


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    order_id = db.Column("order_id", db.Integer)
    where = db.Column("where", db.String)
    recipes = db.relationship("RecipeIngredient",
                              backref="ingredient")


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
