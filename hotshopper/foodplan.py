from hotshopper.model import Recipe


class FoodPlan:
    def __init__(self, shopping_lists):
        self.recipes = []
        self.shopping_lists = shopping_lists

    # def to_dict(self):
    #     return dict(recipes=self.recipes, shopping_lists=self.shopping_lists)

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
        return self.shopping_lists
