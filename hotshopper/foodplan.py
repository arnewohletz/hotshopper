import copy

from hotshopper.ingredients import piece, Supermarket, Market
from hotshopper.recipes import Recipe


class ShoppingList(list):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __contains__(self, type):
        for ingredient in self:
            if isinstance(ingredient, type):
                return True
            return False

    def get_name(self):
        return self.name

    def add(self, ingredient):
        for existing_ingredient in self:
            if ingredient.ingredient.name == existing_ingredient.ingredient.name:
                if ingredient.unit == "piece":
                    existing_ingredient.amount_piece += ingredient.quantity_per_person
                else:
                    existing_ingredient.amount += ingredient.quantity_per_person
                return True
        if ingredient.unit == "piece":
            ingredient.amount_piece = ingredient.quantity_per_person
        else:
            ingredient.amount = ingredient.quantity_per_person
        # Copy required since shopping list otherwise alters the ingredient
        # amount in the recipe, when adding them (not nice, I know)
        self.append(copy.deepcopy(ingredient))

    def sort_ingredients(self):
        self.sort(key=lambda ri: ri.ingredient.id)

    # def substract(self, ingredient):
    #     for existing_ingredient in self:
    #         if isinstance(ingredient, type(existing_ingredient)):
    #             if ingredient.unit.specifier == piece.specifier:
    #               existing_ingredient.amount_piece -= ingredient.amount_piece
    #             else:
    #                 existing_ingredient.amount -= ingredient.amount
    #             if (
    #                 existing_ingredient.amount <= 0 &
    #                 existing_ingredient.amount_piece <= 0
    #             ):
    #                 self.remove(ingredient)


class FoodPlan:
    def __init__(self):
        self.recipes = []
        self.shopping_list_supermarket = ShoppingList("Supermarkt")
        self.shopping_list_market_week1 = ShoppingList("Markt Woche 1")
        self.shopping_list_market_week2 = ShoppingList("Markt Woche 2")
        self.shopping_list_market_week3 = ShoppingList("Markt Woche 3")

    def __add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

        for ri in recipe.ingredients:
            if ri.ingredient.where == "supermarket":
                for i in range(len(recipe.weeks)):
                    self.shopping_list_supermarket.add(ri)
            elif ri.ingredient.where == "market":
                if 1 in recipe.weeks:
                    self.shopping_list_market_week1.add(ri)
                if 2 in recipe.weeks:
                    self.shopping_list_market_week2.add(ri)
                if 3 in recipe.weeks:
                    self.shopping_list_market_week3.add(ri)

    # def __remove_recipe(self, recipe: Recipe):
    #     self.recipes.remove(recipe)
    #
    #     for ingredient in recipe.ingredients:
    #         if isinstance(ingredient.where, Supermarket):
    #             self.shopping_list_supermarket.substract(ingredient)
    #         elif isinstance(ingredient.where, Market):
    #             if 1 in recipe.weeks:
    #                 self.shopping_list_market_week1.substract(ingredient)
    #             if 2 in recipe.weeks:
    #                 self.shopping_list_market_week2.substract(ingredient)
    #             if 3 in recipe.weeks:
    #                 self.shopping_list_market_week3.substract(ingredient)

    def set_shopping_lists(self, recipes: list):
        for recipe in recipes:
            if recipe.selected:
                self.__add_recipe(recipe)

    def get_shopping_lists(self):
        # Currently, sorting the ingredients is done here - not nice
        self.shopping_list_supermarket.sort_ingredients()
        self.shopping_list_market_week1.sort_ingredients()
        self.shopping_list_market_week2.sort_ingredients()
        self.shopping_list_market_week3.sort_ingredients()
        return [
            self.shopping_list_supermarket,
            self.shopping_list_market_week1,
            self.shopping_list_market_week2,
            self.shopping_list_market_week3,
        ]
