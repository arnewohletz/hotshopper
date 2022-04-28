import random
import string

from hotshopper.model import Recipe, RecipeIngredient, Ingredient


def _get_random_string(length: int):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def _get_random_int(min: int, max: int):
    return random.randint(min, max)


def dummy_recipe(weeks: list = None):
    """Create dummy Recipe instance"""
    recipe = Recipe()
    # recipe.id = _get_random_int(0, 1000)
    recipe.name = _get_random_string(10)
    if weeks:
        recipe.weeks = weeks
        recipe.selected = True
    return recipe


def dummy_recipe_ingredient(where: str = "market",
                            quantity_per_person: int = 1,
                            unit: str = "gram"):
    """Create dummy RecipeIngredient"""
    recipe_ingredient = RecipeIngredient()
    recipe_ingredient.ingredient = Ingredient()
    # recipe_ingredient.ingredient.id = _get_random_int(0, 1000)
    recipe_ingredient.ingredient.where = where
    recipe_ingredient.ingredient.name = _get_random_string(10)
    recipe_ingredient.quantity_per_person = quantity_per_person
    recipe_ingredient.unit = unit
    if recipe_ingredient.unit == "gram":
        recipe_ingredient.amount = quantity_per_person
        recipe_ingredient.amount_piece = 0
    else:
        recipe_ingredient.amount_piece = quantity_per_person
        recipe_ingredient.amount = 0

    return recipe_ingredient
