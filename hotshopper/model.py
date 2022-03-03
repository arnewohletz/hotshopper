from pathlib import Path

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from hotshopper import db

Base = declarative_base()

# recipe_ingredient = Table(
#     "recipe_ingredient",
#     Base.metadata,
#     Column("recipe_id", Integer, ForeignKey("recipe.id")),
#     Column("ingredient_id", Integer, ForeignKey("ingredient.id")),
#     Column("amount_per_person", Float),
# )

# recipe_ingredient = db.Table("recipe_ingredient",
#                              db.Column("recipe_id",
#                                        db.Integer,
#                                        db.ForeignKey("recipe.id"),
#                                        primary_key=True),
#                              db.Column("ingredient_id",
#                                        db.Integer,
#                                        db.ForeignKey("ingredient.id"),
#                                        primary_key=True),
#                              db.Column("quantity_per_person",
#                                        db.Integer,
#                                        nullable=False),
#                              db.Column("unit",
#                                        db.String,
#                                        nullable=False))


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"
    # recipe_id = db.Column("recipe.id", db.ForeignKey("recipe.id"), primary_key=True)
    # ingredient_id = db.Column("ingredient.id", db.ForeignKey("ingredient.id"), primary_key=True)
    recipe_id = db.Column(db.ForeignKey("recipe.id"),
                          primary_key=True)
    ingredient_id = db.Column(db.ForeignKey("ingredient.id"),
                              primary_key=True)
    quantity_per_person = db.Column(db.Integer)
    unit = db.Column(db.Integer)
    amount_piece = 0
    amount = 0
    # recipe = db.relationship("Recipe", backref=db.backref("recipes"))
    # ingredient = db.relationship("Ingredient", backref=db.backref("ingredients"))

    # recipe = db.relationship("Recipe", back_populates="recipes")
    # ingredient = db.relationship("Ingredient", back_populates="ingredients")

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


class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # ingredients = relationship("Ingredient", secondary=recipe_ingredient,
    #                            back_populates="recipes")
    # ingredients = db.relationship("Ingredient",
    #                               secondary=recipe_ingredient,
    #                               back_populates="recipes")
    # ingredients = db.relationship("RecipeIngredient",
    #                               back_populates="recipe")
    ingredients = db.relationship("RecipeIngredient",
                                  backref="recipe")
    # ingredients = db.relationship("RecipeIngredient")
    # backref=db.backref("recipes"))

    weeks = []
    selected = False

    def select(self, week: int):
        self.selected = True
        self.weeks.append(week)
        print(self.name + " is selected for week " + str(week))

    def unselect(self, week: int):
        self.weeks.remove(week)
        if len(self.weeks) == 0:
            self.selected = False
        print(self.name + " is deselected from week " + str(week))


class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    order_id = db.Column("order_id", db.Integer)
    where = db.Column("where", db.String)
    # recipes = relationship("Recipe", secondary=recipe_ingredient,
    #                        back_populates="ingredients")
    # recipes = db.relationship("RecipeIngredient",
    #                        back_populates="ingredient")
    # recipes = db.relationship("Recipe",
    #                           secondary=recipe_ingredient,
    #                           back_populates="ingredients")
    # recipes = db.relationship("RecipeIngredient",
    #                           back_populates="ingredient")
    recipes = db.relationship("RecipeIngredient",
                              backref="ingredient")
    # backref=db.backref("ingredients"))


# class RecipeIngredient(db.Model):
#     __tablename__ = "recipe_ingredient"
#     # recipe_id = Column(Integer)
#     # ingredient_id = Column(Integer)
#     recipe_id = db.Column(Integer, db.ForeignKey("recipe.id"), primary_key=True)
#     ingredient_id = db.Column(Integer, db.ForeignKey("ingredient.id"),
#                            primary_key=True)
#     amount_per_person = db.Column(Float)
#     unit = db.Column(String)
#     # recipe = relationship("Recipe", back_populates="ingredients")
#     # ingredient = relationship("Ingredient", back_populates="recipes")
#     ingredient = db.relationship("Ingredient", back_populates="recipes")
#     recipe = db.relationship("Recipe", back_populates="ingredients")


def get_all_ingredients_for_recipe(recipe):
    recipes = (
        db.session.query(Recipe)
        .join(Recipe.ingredients)
        .filter(Recipe.name == recipe.name)
    )
    for recipe in recipes:
        print(f"{recipe.name}")
        for ingredient in recipe.ingredients:
            print(f"{ingredient.ingredient.name}: "
                  f"{ingredient.amount_per_person} "
                  f"{ingredient.unit}")


if __name__ == "__main__":

    # with Path("./recipes.db").resolve() as path:
    #     engine = create_engine(f"sqlite:///{path}")

    # Session = sessionmaker()
    # Session.configure(bind=engine)
    # session = Session()
    all_ingredients = db.session.query(Ingredient).all()
    for ingredient in all_ingredients:
        print(f"{ingredient.name}, {ingredient.order_id}, {ingredient.where}")

    all_recipes = db.session.query(Recipe).all()
    for recipe in all_recipes:
        # print(f"{recipe.name}")
        get_all_ingredients_for_recipe(recipe)
