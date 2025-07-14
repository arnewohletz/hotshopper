# Standard library imports
from typing import List

# Intra-package imports
from hotshopper import logger
from hotshopper.errors import IngredientNotFoundError
from hotshopper.model import Recipe, ShoppingList


class FoodPlan:
    def __init__(self, shopping_lists: List[ShoppingList]):
        self.recipes: List[Recipe] = []
        self.shopping_lists: List[ShoppingList] = shopping_lists

    def _add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

        for week in recipe.weeks:
            for ri in recipe.ingredients:
                for shopping_list in self.shopping_lists:
                    if (shopping_list.has_location(ri.ingredient.location_id)
                            and shopping_list.has_week(week)):
                        try:
                            shopping_list.add(ri)
                        except IngredientNotFoundError:
                            logger.error(
                                f"Ingredient {ri!r} not added to"
                                f"shopping list '{shopping_list.name}'")
                        break

    def set_shopping_lists(self, recipes: List[Recipe]):
        for recipe in recipes:
            if recipe.selected:
                self._add_recipe(recipe)

    def get_shopping_lists(self):
        return self.shopping_lists
