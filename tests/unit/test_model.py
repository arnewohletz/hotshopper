import pytest

from hotshopper import model
from tests.unit import helper


class TestRecipe:
    # INCOMING COMMANDS

    # @pytest.fixture(scope="function")
    # def dummy_recipe(self):
    #     """Create dummy Recipe instance"""
    #     recipe = model.Recipe()
    #     recipe.name = "NOT_IMPORTANT"
    #     return recipe

    def test_recipe_select(self):
        selected_weeks = [1, 3]
        dummy_recipe = helper.dummy_recipe(weeks=selected_weeks)
        assert dummy_recipe.selected
        assert dummy_recipe.weeks == selected_weeks

    def test_recipe_unselect(self):
        dummy_recipe = helper.dummy_recipe()
        dummy_recipe.select(1)
        dummy_recipe.unselect(1)
        assert dummy_recipe.weeks is None
        assert not dummy_recipe.selected


class TestIngredientRecipe:

    def test_get_gram_amount(self):
        gram_amount = 100
        recipe_ingredient = helper.dummy_recipe_ingredient(
            quantity_per_person=gram_amount, unit="gram")
        assert recipe_ingredient.get_amount() == 100

    def test_get_piece_amount(self):
        piece_amount = 5
        recipe_ingredient = helper.dummy_recipe_ingredient(
            quantity_per_person=piece_amount, unit="piece")
        assert recipe_ingredient.get_amount() == 5


def _get_dummy_recipe_ingredient(amount: int = 0,
                                 amount_piece: int = 0,
                                 ) -> model.RecipeIngredient:
    ingredient = model.RecipeIngredient()
    ingredient.amount = amount
    ingredient.amount_piece = amount_piece
    return ingredient
