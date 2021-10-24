from hotshopper.foodplan import FoodPlan
from hotshopper.recipes import *


# working
def test_add_single_recipe_to_shopping_list():
    food_plan = FoodPlan()
    recipes = [PotatoSoup()]
    for recipe in recipes:
        recipe.select(week=1)
    food_plan.set_shopping_lists(recipes)

    for shopping_list in food_plan.get_shopping_lists():
        for ingredient in shopping_list:
            if any(isinstance(ingredient, type(item)) for item in
                   PotatoSoup().ingredients):
                i = PotatoSoup().ingredients[type(ingredient)]

                assert ingredient.get_amount() == i.get_amount()
            else:
                assert False


# working
def test_two_combined_quantities_on_shopping_list():
    food_plan = FoodPlan()
    recipes = [PotatoSoup(), CheeseNoodles()]
    onions_amount_recipe = 0
    for recipe in recipes:
        recipe.select(week=1)
        onions_amount_recipe += recipe.ingredients[Onion].get_amount()

    for shopping_list in food_plan.get_shopping_lists():
        for ingredient in shopping_list:
            if isinstance(ingredient, Onion):
                food_plan_onions_amount = ingredient.get_amount()
                assert onions_amount_recipe == food_plan_onions_amount


def test_remove_recipe_from_food_plan():
    parsley_root_curry = ParsleyRootCurry()
    potato_soup = PotatoSoup()
    parsley_root_curry.select(week=1)
    potato_soup.select(week=1)
    potato_soup.unselect(week=1)

    food_plan = FoodPlan()
    food_plan.set_shopping_lists([parsley_root_curry, potato_soup])
    assert parsley_root_curry.selected
    assert not potato_soup.selected


# def test_remove_recipe_from_shopping_list():
#     food_plan = FoodPlan()
#     food_plan.add_recipe(ParsleyRootCurry(week=2))
#     food_plan.add_recipe(PotatoSoup(week=1))
#     food_plan.remove_recipe(PotatoSoup(week=1))
#     assert (food_plan.shopping_list.items, ParsleyRootCurry().ingredients)

