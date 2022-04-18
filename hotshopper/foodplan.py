from hotshopper.model import Recipe, ShoppingListIngredient


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
            if ingredient.ingredient.name == existing_ingredient.name:
                if ingredient.unit == "st.":
                    existing_ingredient.amount_piece += ingredient.amount_piece
                else:
                    existing_ingredient.amount += ingredient.amount
                return True
        self.append(ShoppingListIngredient(ingredient))
        # Copy required since shopping list otherwise alters the ingredient
        # amount in the recipe, when adding them (not nice, I know)
        # self.append(copy.deepcopy(ingredient))

    def sort_ingredients(self):
        self.sort(key=lambda ri: ri.order_id)


class FoodPlan:
    def __init__(self):
        self.recipes = []
        self.shopping_list_supermarket = ShoppingList("Supermarkt")
        self.shopping_list_market_week1 = ShoppingList("Markt Woche 1")
        self.shopping_list_market_week2 = ShoppingList("Markt Woche 2")
        self.shopping_list_market_week3 = ShoppingList("Markt Woche 3")

    def _add_recipe(self, recipe: Recipe):
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

    def set_shopping_lists(self, recipes: list):
        for recipe in recipes:
            if recipe.selected:
                self._add_recipe(recipe)

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
