from dataclasses import dataclass

from hotshopper.constants import Unit, Location
from hotshopper.model import Recipe, ShoppingListItem, Location, ShoppingList


# class ShoppingList(list):
#
#     def __init__(self, name, locations, weeks):
#         super().__init__()
#         self.name = name
#         self.locations = locations
#         self.weeks = weeks
#
#     def __contains__(self, type):
#         for ingredient in self:
#             if isinstance(ingredient, type):
#                 return True
#             return False
#
#     def get_name(self):
#         return self.name
#
#     def add(self, ingredient):
#         if ingredient.unit == Unit.PIECE:
#             ingredient.amount_piece = ingredient.quantity_per_person
#         else:
#             ingredient.amount = ingredient.quantity_per_person
#
#         for existing_ingredient in self:
#             if ingredient.ingredient.name == existing_ingredient.name:
#                 if ingredient.unit == Unit.PIECE:
#                     # TODO: Add multiplied by 'persons' once added to recipe
#                     existing_ingredient.amount_piece += ingredient.amount_piece
#                 else:
#                     existing_ingredient.amount += ingredient.amount
#                 return True
#         self.append(ShoppingListIngredient(ingredient))
        # Copy required since shopping list otherwise alters the ingredient
        # amount in the recipe, when adding them (not nice, I know)
        # self.append(copy.deepcopy(ingredient))

    # def sort_ingredients(self):
    #     self.sort(key=lambda ri: ri.order_id)
    #
    # def append_always_on_list_items(self):
    #     # TODO: Implement append_always_on_list_items() method
    #     raise NotImplementedError

class FoodPlan:
    def __init__(self, shopping_lists):
        self.recipes = []
        self.shopping_lists = shopping_lists
        # self.shopping_list_supermarket = ShoppingList("Supermarkt",
        #                                               locations=[
        #                                                   Location.query.filter_by(
        #                                                       name="Supermarkt")],
        #                                               weeks=[1, 2, 3])
        # self.shopping_list_market_week1 = ShoppingList("Markt Woche 1",
        #                                                locations=[
        #                                                    Location.query.filter_by(
        #                                                        name=["Markt",
        #                                                              "Metzger",
        #                                                              "Bäcker"])],
        #                                                weeks=[1]),
        # self.shopping_list_market_week2 = ShoppingList("Markt Woche 2",
        #                                                locations=[
        #                                                    Location.query.filter_by(
        #                                                        name=["Markt",
        #                                                              "Metzger",
        #                                                              "Bäcker"])],
        #                                                weeks=[2]),
        # self.shopping_list_market_week3 = ShoppingList("Markt Woche 3",
        #                                                locations=[
        #                                                    Location.query.filter_by(
        #                                                        name=["Markt",
        #                                                              "Metzger",
        #                                                              "Bäcker"])],
        #                                                weeks=[3]),
    def to_dict(self):
        return dict(recipes=self.recipes, shopping_lists=self.shopping_lists)

    def _add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

        for week in recipe.weeks:
            for ri in recipe.ingredients:
                for shopping_list in self.shopping_lists:
                    if shopping_list.has_location(ri.ingredient.location_id) \
                        and shopping_list.has_week(week):
                        # TODO: Only add ingredient if shopping list has correct week
                        shopping_list.add(ri)
                        # TODO: I have everything here:
                        #   ri -> ingredient.location_id, ingredient.location.section.id
                        #   self ->  [shopping_lists].id
                        #  Must find a way to add ri to the correct shopping_list.location.section
                        #  so it is already placed correctly for printing shopping list
                        break
            # if self.shopping_listsri.ingredient.location_id in self.shopping_lists.locations.idsupermarket.locations:
            #     for i in range(len(recipe.weeks)):
            #         self.shopping_list_supermarket.add(ri)
            # # elif ri.ingredient.location_id in self.:
            # else:
            #     if 1 in recipe.weeks:
            #         self.shopping_list_market_week1.add(ri)
            #     if 2 in recipe.weeks:
            #         self.shopping_list_market_week2.add(ri)
            #     if 3 in recipe.weeks:
            #         self.shopping_list_market_week3.add(ri)

    def set_shopping_lists(self, recipes: list):
        for recipe in recipes:
            if recipe.selected:
                self._add_recipe(recipe)

    def get_shopping_lists(self):
        # Currently, sorting the ingredients is done here - not nice
        for shopping_list in self.shopping_lists:
            shopping_list.sort_ingredients()
        return self.shopping_lists
        # self.shopping_list_supermarket.sort_ingredients()
        # self.shopping_list_market_week1.sort_ingredients()
        # self.shopping_list_market_week2.sort_ingredients()
        # self.shopping_list_market_week3.sort_ingredients()
        # return [
        #     self.shopping_list_supermarket,
        #     self.shopping_list_market_week1,
        #     self.shopping_list_market_week2,
        #     self.shopping_list_market_week3,
        # ]
