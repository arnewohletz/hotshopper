from pathlib import Path

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, reconstructor

from hotshopper import db

Base = declarative_base()

# recipe_ingredient = Table(
#     "recipe_ingredient",
#     Base.metadata,
#     Column("recipe_id", Integer, ForeignKey("recipe.id")),
#     Column("ingredient_id", Integer, ForeignKey("ingredient.id")),
#     Column("amount_per_person", Float),
# )


class Location:
    pass


class Supermarket(Location):
    pass


class Market(Location):
    pass


class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    # ingredients = relationship("Ingredient", secondary=recipe_ingredient,
    #                            back_populates="recipes")
    ingredients = db.relationship("RecipeIngredient",
                                  back_populates="recipe")
    selected = False
    weeks = []

    def __init__(self):
        self.db_init(self)

    @reconstructor
    def db_init(self):
        self.selected = False
        self.weeks = []

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
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    order_id = db.Column(Integer)
    where = db.Column(String)
    # recipes = relationship("Recipe", secondary=recipe_ingredient,
    #                        back_populates="ingredients")
    recipes = db.relationship("RecipeIngredient",
                              back_populates="ingredient")


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"
    # recipe_id = Column(Integer)
    # ingredient_id = Column(Integer)
    recipe_id = db.Column(Integer, db.ForeignKey("recipe.id"),
                          primary_key=True)
    ingredient_id = db.Column(Integer, db.ForeignKey("ingredient.id"),
                              primary_key=True)
    amount_per_person = db.Column(Float)
    unit = db.Column(String)
    # recipe = relationship("Recipe", back_populates="ingredients")
    # ingredient = relationship("Ingredient", back_populates="recipes")
    ingredient = db.relationship("Ingredient", back_populates="recipes")
    recipe = db.relationship("Recipe", back_populates="ingredients")

    total_amount_gram_recipes = 0
    total_amount_piece_recipes = 0.0

    def __init__(self):
        self.db_init(self)

    @reconstructor
    def db_init(self):
        self.total_amount_gram_recipes = 0
        self.total_amount_piece_recipes = 0.0

    # def __init__(self):
    #     if ingredient.where == "supermarket":
    #         self.where = Supermarket()
    #     elif ingredient.where == "market":
    #         self.where = Market()

    def get_amount(self):
        if self.total_amount_piece_recipes > 0:
            if float(self.total_amount_piece_recipes).is_integer():
                return int(self.total_amount_piece_recipes)
            else:
                return self.total_amount_piece_recipes
        elif self.total_amount_gram_recipes > 0:
            if float(self.total_amount_gram_recipes).is_integer():
                return int(self.total_amount_gram_recipes)
            else:
                return self.total_amount_gram_recipes
        else:
            return 0


def get_all_ingredients_for_recipe(session, recipe):
    recipes = (
        session.query(Recipe)
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

    with Path("./recipes.db").resolve() as path:
        engine = create_engine(f"sqlite:///{path}")

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    all_ingredients = session.query(Ingredient).all()
    for ingredient in all_ingredients:
        print(f"{ingredient.name}, {ingredient.order_id}, {ingredient.where}")

    all_recipes = session.query(Recipe).all()
    for recipe in all_recipes:
        # print(f"{recipe.name}")
        get_all_ingredients_for_recipe(session, recipe)
