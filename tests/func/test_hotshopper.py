import pytest
from hotshopper.hotshopper import ShoppingList
from hotshopper.ingredients import Carrot
from hotshopper.recipes import PotatoSoup


def test_add_recipe_to_shopping_list():
    shopping_list = ShoppingList()
    recipe = PotatoSoup()

    shopping_list.add_recipe(recipe)
    assert(any(isinstance(x, Carrot) for x in shopping_list.items))
    for recipe in shopping_list.recipes:
        recipe.print_ingredients()

