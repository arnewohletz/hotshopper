import pytest
import random
import string

from hotshopper import db, create_app
from hotshopper.constants import Location, Unit
from hotshopper.foodplan import FoodPlan
from tests.unit import helper


def get_random_string(length: int):
    """
    Returns a string of given length.

    :param length: length of the returned string
    :return: str
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@pytest.fixture
def app():
    return create_app(test=True)


@pytest.fixture(scope="function")
def setup_teardown():
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


@pytest.fixture
def td():
    return helper.TestDataGenerator(db)


class TestFoodPlan:

    def test_add_selected_recipe(self, app, setup_teardown, td):
        r_id = td.create_recipe()
        i1_id = td.create_ingredient(where=Location.MARKET)
        i2_id = td.create_ingredient(where=Location.SUPERMARKET)
        td.create_recipe_ingredient(recipe_id=r_id, ingredient_id=i1_id)
        td.create_recipe_ingredient(recipe_id=r_id, ingredient_id=i2_id)

        recipe = td.get_recipe(recipe_id=r_id)
        recipe.select(week=1)
        recipe.select(week=2)

        foodplan = FoodPlan()
        foodplan.set_shopping_lists([recipe])

        assert len(foodplan.recipes) == 1
        assert len(foodplan.shopping_list_supermarket) == 1
        assert len(foodplan.shopping_list_market_week1) == 1
        assert len(foodplan.shopping_list_market_week2) == 1
        assert len(foodplan.shopping_list_market_week3) == 0

    def test_omit_unselected_recipe(self, app, setup_teardown, td):
        r_id = td.create_recipe()
        i1_id = td.create_ingredient(where=Location.MARKET)
        td.create_recipe_ingredient(recipe_id=r_id, ingredient_id=i1_id)
        recipe = td.get_recipe(recipe_id=r_id)

        foodplan = FoodPlan()
        foodplan.set_shopping_lists([recipe])

        assert len(foodplan.recipes) == 0
        assert len(foodplan.shopping_list_supermarket) == 0
        assert len(foodplan.shopping_list_market_week1) == 0
        assert len(foodplan.shopping_list_market_week2) == 0
        assert len(foodplan.shopping_list_market_week3) == 0


class TestShoppingList:

    def test_same_ingredients_are_added(self, app, setup_teardown, td):
        r1_id = td.create_recipe()
        r2_id = td.create_recipe()
        i1_id = td.create_ingredient(where=Location.MARKET, name="ABC")
        i2_id = td.create_ingredient(where=Location.SUPERMARKET, name="CBA")
        td.create_recipe_ingredient(recipe_id=r1_id,
                                    ingredient_id=i1_id,
                                    quantity_per_person=100,
                                    unit=Unit.GRAM)
        td.create_recipe_ingredient(recipe_id=r2_id,
                                    ingredient_id=i1_id,
                                    quantity_per_person=100,
                                    unit=Unit.GRAM)
        td.create_recipe_ingredient(recipe_id=r1_id,
                                    ingredient_id=i2_id,
                                    quantity_per_person=10,
                                    unit=Unit.PIECE)
        td.create_recipe_ingredient(recipe_id=r2_id,
                                    ingredient_id=i2_id,
                                    quantity_per_person=10,
                                    unit=Unit.PIECE)
        r1 = td.get_recipe(recipe_id=r1_id)
        r2 = td.get_recipe(recipe_id=r2_id)
        r1.select(week=1)
        r2.select(week=1)

        foodplan = FoodPlan()
        foodplan.set_shopping_lists([r1, r2])
        sli1 = foodplan.shopping_list_market_week1[0]
        sli2 = foodplan.shopping_list_supermarket[0]

        assert sli1.name == "ABC"
        assert sli1.print_amounts() == 200
        assert sli2.name == "CBA"
        assert sli2.print_amounts() == 20

    def test_gram_piece_amount_are_summed_separately(self, app, setup_teardown,
                                                     td):
        r1_id = td.create_recipe()
        r2_id = td.create_recipe()
        i1_id = td.create_ingredient(where=Location.SUPERMARKET, name="ABC")
        td.create_recipe_ingredient(recipe_id=r1_id,
                                    ingredient_id=i1_id,
                                    quantity_per_person=100,
                                    unit=Unit.GRAM)
        td.create_recipe_ingredient(recipe_id=r2_id,
                                    ingredient_id=i1_id,
                                    quantity_per_person=1,
                                    unit=Unit.PIECE)

        r1 = td.get_recipe(recipe_id=r1_id)
        r2 = td.get_recipe(recipe_id=r2_id)
        r1.select(week=1)
        r2.select(week=1)

        foodplan = FoodPlan()
        foodplan.set_shopping_lists([r1, r2])
        sli = foodplan.shopping_list_supermarket[0]

        assert sli.amount == 100
        assert sli.amount_piece == 1

    def test_ingredients_of_deselected_recipes_are_removed(self, app,
                                                           setup_teardown,
                                                           td):
        r1_id = td.create_recipe()
        r2_id = td.create_recipe()
        i1_id = td.create_ingredient(where=Location.SUPERMARKET, name="ABC")
        td.create_recipe_ingredient(recipe_id=r1_id,
                                    ingredient_id=i1_id,
                                    quantity_per_person=100,
                                    unit=Unit.GRAM)
        td.create_recipe_ingredient(recipe_id=r2_id,
                                    ingredient_id=i1_id,
                                    quantity_per_person=100,
                                    unit=Unit.GRAM)
        r1 = td.get_recipe(recipe_id=r1_id)
        r2 = td.get_recipe(recipe_id=r2_id)
        r1.select(week=1)
        r2.select(week=1)
        r2.unselect(week=1)

        foodplan = FoodPlan()
        foodplan.set_shopping_lists([r1, r2])
        sli = foodplan.shopping_list_supermarket[0]

        assert sli.amount == 100
