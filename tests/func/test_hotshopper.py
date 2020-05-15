from hotshopper.foodplan import FoodPlan
from hotshopper.ingredients import Carrot
from hotshopper.recipes import PotatoSoup, ParsleyRootCurry


def test_add_recipe_to_shopping_list():
    food_plan = FoodPlan()
    food_plan.add_recipe(PotatoSoup())
    assert(any(isinstance(x, Carrot) for x in food_plan.shopping_list))
    food_plan.shopping_list.print_ingredients()


def test_two_combined_quantities_on_shopping_list():
    food_plan = FoodPlan()
    food_plan.add_recipe(ParsleyRootCurry())
    food_plan.add_recipe(PotatoSoup())
    food_plan.shopping_list.print_ingredients()
    assert True
