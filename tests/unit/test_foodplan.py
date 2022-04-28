import random
import string

# from hotshopper.model import Recipe, RecipeIngredient
from hotshopper.foodplan import FoodPlan
from tests.unit import helper


def get_random_string(length: int):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class TestFoodPlan:

    def test_add_recipe(self):
        r_a = helper.dummy_recipe(weeks=[1])
        r_b = helper.dummy_recipe(weeks=[2])
        r_c = helper.dummy_recipe(weeks=[1, 3])

        ri_a = helper.dummy_recipe_ingredient()
        ri_b = helper.dummy_recipe_ingredient()
        ri_c = helper.dummy_recipe_ingredient()

        r_a.ingredients.append(ri_a)
        r_b.ingredients.append(ri_b)
        r_c.ingredients.append(ri_c)

        foodplan = FoodPlan()
        foodplan._add_recipe(r_a)
        foodplan._add_recipe(r_b)
        foodplan._add_recipe(r_c)

        assert len(foodplan.recipes) == 3
        assert len(foodplan.shopping_list_market_week1) == 2
        assert len(foodplan.shopping_list_market_week2) == 1
        assert len(foodplan.shopping_list_market_week3) == 1
