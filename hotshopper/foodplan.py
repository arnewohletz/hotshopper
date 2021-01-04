from hotshopper.recipes import Recipe
from hotshopper.ingredients import piece, Supermarket, Market


class ShoppingList:

    def __init__(self, name):
        self.name = name
        # TODO: Problem: ShoppingList(list) cannot store a 'name' variable

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


class ShoppingList(list):

    def __contains__(self, type):
        for ingredient in self:
            if isinstance(ingredient, type):
                return True
            return False

    # TODO: Does it work like this:???

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

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
        self.shopping_list_supermarket = ShoppingList()
        self.shopping_list_market_week1 = ShoppingList()
        self.shopping_list_market_week2 = ShoppingList()
        self.shopping_list_market_week3 = ShoppingList()

    def __add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

        for ingredient in recipe.ingredients:
            # TODO: add ingredient to proper shopping list
            if isinstance(ingredient.where, Supermarket):
                self.shopping_list_supermarket.add(ingredient)
            elif isinstance(ingredient.where, Market):
                if recipe.week == 1:
                    self.shopping_list_market_week1.add(ingredient)
                elif recipe.week == 2:
                    self.shopping_list_market_week2.add(ingredient)
                elif recipe.week == 3:
                    self.shopping_list_market_week3.add(ingredient)
            # self.shopping_list.add(ingredient)

    def __remove_recipe(self, recipe: Recipe):
        self.recipes.remove(recipe)

        for ingredient in recipe.ingredients:
            # TODO: Remove ingredient from proper shopping list
            if isinstance(ingredient.where, Supermarket):
                self.shopping_list_supermarket.substract(ingredient)
            elif isinstance(ingredient.where, Market):
                if recipe.week == 1:
                    self.shopping_list_market_week1.substract(ingredient)
                elif recipe.week == 2:
                    self.shopping_list_market_week2.substract(ingredient)
                elif recipe.week == 3:
                    self.shopping_list_market_week3.substract(ingredient)
            # self.shopping_list.substract(ingredient)

    def set_shopping_lists(self, recipes: list):
        # TODO: add additional shopping lists
        # self.recipes = []
        # self.shopping_list = ShoppingList()
        for recipe in recipes:
            if recipe.selected:
                self.__add_recipe(recipe)

    def get_shopping_lists(self):
        # TODO: Add additional shopping lists
        return [self.shopping_list_supermarket,
                self.shopping_list_market_week1,
                self.shopping_list_market_week2,
                self.shopping_list_market_week3]
