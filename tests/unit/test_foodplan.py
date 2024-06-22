
# Third-party library imports
import pytest

# Intra-package imports
from hotshopper.foodplan import FoodPlan
from hotshopper.model import Recipe, ShoppingList


@pytest.fixture
def three_recipes():
    recipe_1 = Recipe(name="some_name")
    recipe_2 = Recipe(name="some_other_name")
    recipe_3 = Recipe(name="yet_another_name")
    return [recipe_1, recipe_2, recipe_3]


class TestFoodPlan:

    def test_get_shopping_lists(self):
        shopping_list_1 = ShoppingList(name="some_name")
        shopping_list_2 = ShoppingList(name="some_other_name")
        shopping_list_3 = ShoppingList(name="yet_another_name")
        foodplan = FoodPlan([shopping_list_1,
                             shopping_list_2,
                             shopping_list_3])

        amount_shopping_lists = len(foodplan.get_shopping_lists())

        assert amount_shopping_lists == 3

    def test_set_empty_recipes_list(self):
        shopping_list = ShoppingList(name="some_name")

        foodplan = FoodPlan([shopping_list])
        foodplan.set_shopping_lists([])

        assert len(foodplan.recipes) == 0

    def test_set_recipes(self, three_recipes):
        shopping_list = ShoppingList(name="some_name")
        food_plan = FoodPlan(shopping_lists=[shopping_list])

        three_recipes[0].select(week=1)
        three_recipes[1].select(week=2)
        three_recipes[2].select(week=3)
        food_plan.set_shopping_lists(recipes=three_recipes)

        assert len(food_plan.recipes) == 3

    def test_omit_unselected_recipes(self, three_recipes):
        shopping_list = ShoppingList(name="some_name")
        food_plan = FoodPlan(shopping_lists=[shopping_list])

        three_recipes[0].select(week=1)
        three_recipes[1].select(week=2)
        three_recipes[2].select(week=3)

        three_recipes[0].unselect(week=1)
        food_plan.set_shopping_lists(recipes=three_recipes)

        assert len(food_plan.recipes) == 2
