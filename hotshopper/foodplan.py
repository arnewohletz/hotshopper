from hotshopper.recipes import Recipe
from hotshopper.ingredients import piece


class ShoppingList(list):

    def __contains__(self, type):
        for ingredient in self:
            if isinstance(ingredient, type):
                return True
            return False

    def add(self, ingredient):
        for existing_ingredient in self:
            if isinstance(ingredient, type(existing_ingredient)):
                if ingredient.unit.specifier == piece.specifier:
                    existing_ingredient.amount_piece += ingredient.amount_piece
                else:
                    existing_ingredient.amount += ingredient.amount
                return True
        self.append(ingredient)

    def substract(self, ingredient):
        for existing_ingredient in self:
            if isinstance(ingredient, type(existing_ingredient)):
                if ingredient.unit.specifier == piece.specifier:
                    existing_ingredient.amount_piece -= ingredient.amount_piece
                else:
                    existing_ingredient.amount -= ingredient.amount
                if existing_ingredient.amount <= 0 \
                        & existing_ingredient.amount_piece <= 0:
                    self.remove(ingredient)


class FoodPlan:

    def __init__(self):
        self.recipes = []
        self.shopping_list = ShoppingList()

    def __add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

        for ingredient in recipe.ingredients:
            self.shopping_list.add(ingredient)

    def __remove_recipe(self, recipe: Recipe):
        self.recipes.remove(recipe)

        for ingredient in recipe.ingredients:
            self.shopping_list.substract(ingredient)

    def set_shopping_list(self, recipes: list):
        self.recipes = []
        self.shopping_list = ShoppingList()
        for recipe in recipes:
            if recipe.selected:
                self.__add_recipe(recipe)

    def get_shopping_list(self):
        return self.shopping_list
