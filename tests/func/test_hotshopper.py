from hotshopper.foodplan import FoodPlan
from hotshopper.ingredients import Carrot
from hotshopper.recipes import *


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


def test_remove_recipe_from_shopping_list():
    food_plan = FoodPlan()
    food_plan.add_recipe(ParsleyRootCurry())
    food_plan.add_recipe(PotatoSoup())
    food_plan.remove_recipe(PotatoSoup())
    assert(food_plan.shopping_list.items, ParsleyRootCurry().ingredients)


def test_correct_ingredients_market_1():
    food_plan = FoodPlan()

    salad = SaladAndMaultaschen()
    salad.set_selected(True, week=1)
    salad.set_selected(True, week=2)
    salad.set_selected(True, week=3)

    chicoree = ChicoryWithHam()
    chicoree.set_selected(True, week=1)

    recipes = [salad, chicoree]
    food_plan.set_shopping_lists(recipes)

    assert food_plan.shopping_list_market_week1 != \
           food_plan.shopping_list_market_week2
