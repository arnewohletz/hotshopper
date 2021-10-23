from hotshopper.foodplan import FoodPlan
from hotshopper.recipes import *


# working
def test_add_single_recipe_to_shopping_list():
    food_plan = FoodPlan()
    recipes = [PotatoSoup()]
    for recipe in recipes:
        recipe.select(True, week=1)
    food_plan.set_shopping_lists(recipes)

    for shopping_list in food_plan.get_shopping_lists():
        for ingredient in shopping_list:
            if any(isinstance(ingredient, type(item)) for item in
                   PotatoSoup().ingredients):
                i = PotatoSoup().ingredients[ingredient]
                assert ingredient.get_amount() == i.get_amount()
            else:
                assert False


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
    assert (food_plan.shopping_list.items, ParsleyRootCurry().ingredients)


def test_correct_ingredients_market_1():
    food_plan = FoodPlan()

    salad = SaladAndMaultaschen()
    salad.select(True, week=1)
    salad.select(True, week=2)
    salad.select(True, week=3)

    chicoree = ChicoryWithHam()
    chicoree.select(True, week=1)

    recipes = [salad, chicoree]
    food_plan.set_shopping_lists(recipes)

    assert food_plan.shopping_list_market_week1 != \
           food_plan.shopping_list_market_week2
