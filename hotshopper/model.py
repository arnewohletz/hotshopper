from pathlib import Path

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from hotshopper.hotshopper import app, db

Base = declarative_base()

# recipe_ingredient = Table(
#     "recipe_ingredient",
#     Base.metadata,
#     Column("recipe_id", Integer, ForeignKey("recipe.id")),
#     Column("ingredient_id", Integer, ForeignKey("ingredient.id")),
#     Column("amount_per_person", Float),
# )


class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # ingredients = relationship("Ingredient", secondary=recipe_ingredient,
    #                            back_populates="recipes")
    ingredients = relationship("RecipeIngredient",
                               back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredient"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    order_id = Column(Integer)
    where = Column(String)
    # recipes = relationship("Recipe", secondary=recipe_ingredient,
    #                        back_populates="ingredients")
    recipes = relationship("RecipeIngredient",
                           back_populates="ingredient")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"
    # recipe_id = Column(Integer)
    # ingredient_id = Column(Integer)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"),
                           primary_key=True)
    amount_per_person = Column(Float)
    unit = Column(String)
    # recipe = relationship("Recipe", back_populates="ingredients")
    # ingredient = relationship("Ingredient", back_populates="recipes")
    ingredient = relationship("Ingredient", back_populates="recipes")
    recipe = relationship("Recipe", back_populates="ingredients")


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
