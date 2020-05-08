"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ingredients import Ingredient, gram, kilogram, piece


def main():
    pass


class ShoppingList:
    recipes = []
    items = []

    def add_recipe(self, recipe: Recipe):

        for ingredient in recipe.ingredients:
            self.recipes.append(recipe)
            self._add_ingredient(ingredient)

    def _add_ingredient(self, ingredient):
        # Note: when adding units, the first unit is used for the result
        item = self.get_item(ingredient)
        if item:
            if isinstance(ingredient.unit, piece):
                item.amount_piece += ingredient.amount_piece
            elif isinstance(ingredient.unit, (gram, kilogram)):
                item.amount_weigth += ingredient.amount_weight
        else:
            self.items.append(ingredient)

    def get_item(self, ingredient: Ingredient):

        for item in self.items:
            if type(item) == type(ingredient):
                return item



