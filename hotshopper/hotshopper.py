"""Main module."""
from hotshopper.recipes import Recipe
from hotshopper.ingredients import kilogram, piece


def main():
    pass


class ShoppingList(list):
    recipes = []
    items = []

    def __contains__(self, type):
        for ingredient in self:
            if isinstance(ingredient, type):
                return True
            return False

    def add(self, ingredient):
        for existing_ingredient in self:
            if isinstance(ingredient, type(existing_ingredient)):
                existing_ingredient.amount += ingredient.amount
                return True
        self.append(ingredient)

    def print_ingredients(self):

        print("\n")

        for ingredient in self:
            if ingredient.unit == kilogram:
                print(f"{ingredient.amount} {ingredient.name}")
            if ingredient.unit == piece:
                print(f"{ingredient.amount.num} {ingredient.name}")
            else:
                print(f"{int(ingredient.amount.num)} "
                        f"{ingredient.amount.unit} "
                        f"{ingredient.name}")


class FoodPlan:

    def __init__(self):
        self.recipes = []
        self.shopping_list = ShoppingList()

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

        for ingredient in recipe.ingredients:
            self.shopping_list.add(ingredient)
