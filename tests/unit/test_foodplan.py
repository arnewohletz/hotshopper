import pytest
import random
import string

# from pathlib import Path
# from sqlalchemy import create_engine, MetaData
# from flask_sqlalchemy import SQLAlchemy

from hotshopper import get_db, get_app
from hotshopper.foodplan import FoodPlan
from hotshopper.model import Location, Recipe, ShoppingList, Week
from tests.unit import helper


# app = get_app()
# _db = get_db()

# @pytest.fixture
# def test_db():
#     # Configuration for the test database
#     with Path(__file__).parent.resolve() / "test_recipes.db" as test_path:
#         app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{test_path}?check_same_thread=False"
#
#     # Create a new engine and session for the test database
#     test_db = SQLAlchemy(app, session_options={"autoflush": False})
#     test_engine = test_db.engine
#     test_metadata = test_db.metadata
#
#     # Reflect the original database schema into the metadata
#     test_metadata.reflect()
#
#     # Create tables in the test database
#     test_metadata.create_all(test_engine)
#
#     # Copy data from the original to the test database
#     with app.app_context():
#         with _db.engine.connect() as orig_conn, test_engine.connect() as test_conn:
#             for table in test_metadata.sorted_tables:
#                 data = orig_conn.execute(table.select()).fetchall()
#                 test_conn.execute(table.insert().values(data))
#
#     return test_db



def get_random_string(length: int):
    """
    Returns a string of given length.

    :param length: length of the returned string
    :return: str
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_app():
    app = get_app()
    # Use the testing configuration and an in-memory SQLite database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app


# @pytest.fixture(scope="function")
@pytest.fixture()
def test_db():
    test_db = get_db()
    test_db.create_all()
    yield test_db
    test_db.session.remove()
    test_db.drop_all()


# @pytest.fixture
def random_test_data_generator(test_db):
    return helper.RandomTestDataGenerator(test_db)


class TestFoodPlan:
    def test_get_shopping_list(self, test_db):
        tdg = random_test_data_generator(test_db)
        s = tdg.create_shopping_list()
        foodplan = FoodPlan([s])
        amount_shopping_lists = len(foodplan.get_shopping_lists())

        assert amount_shopping_lists == 1

    def test_no_recipe_selected(self, test_db):
        sl_s = ShoppingList(name="supermarket",
                            locations=[
                                Location(name="supermarket", order_id=1)],
                            weeks=[Week(number=1), Week(number=2),
                                   Week(number=3)],
                            print_columns=1)
        foodplan = FoodPlan([sl_s])
        foodplan.set_shopping_lists([])

        assert len(foodplan.recipes) == 0

    def test_single_recipe_selected(self, test_db):
        tdg = random_test_data_generator(test_db)
        r = tdg.create_recipe()
        r_id = r.add()

        recipe = Recipe.query.filter_by(id=r_id).first()
        recipe.select(week=1)

        sl_s = ShoppingList(name="supermarket",
                            locations=[Location(name="supermarket", order_id=1)],
                            weeks=[Week(number=1), Week(number=2), Week(number=3)],
                            print_columns=1)
        foodplan = FoodPlan([sl_s])
        foodplan.set_shopping_lists([recipe])

        assert len(foodplan.recipes) == 1
        assert foodplan.recipes[0].weeks == [1]

    def test_single_recipe_multiple_weeks_selected(self, test_db):
        tdg = random_test_data_generator(test_db)

        r = tdg.create_recipe()
        r.select(week=1)
        r.select(week=2)

        sl_s = ShoppingList(name="supermarket",
                            locations=[
                                Location(name="supermarket", order_id=1)],
                            weeks=[Week(number=1), Week(number=2)],
                            print_columns=1)
        foodplan = FoodPlan([sl_s])
        foodplan.set_shopping_lists([r])

        assert len(foodplan.recipes) == 1
        assert foodplan.recipes[0].weeks == [1, 2]

    def test_unselected_recipe_is_omitted(self, test_db):
        tdg = random_test_data_generator(test_db)
        r = tdg.create_recipe()
        r_id = r.add()

        recipe = Recipe.query.filter_by(id=r_id).first()
        recipe.select(week=1)
        recipe.unselect(week=1)

        sl_s = ShoppingList(name="supermarket",
                            locations=[Location(name="supermarket", order_id=1)],
                            weeks=[Week(number=1), Week(number=2), Week(number=3)],
                            print_columns=1)
        foodplan = FoodPlan([sl_s])
        assert len(foodplan.recipes) == 0
