
# Third-party library imports
import pytest

# Intra-package imports
from hotshopper.foodplan import FoodPlan
from hotshopper.model import (
    Ingredient,
    Location,
    Recipe,
    RecipeIngredient,
    Section,
    ShoppingList,
    ShoppingListLocation,
    ShoppingListWeek,
    Week
)
from tests.unit.helper import get_random_int


@pytest.fixture
def three_recipes():
    recipe_1 = Recipe(name="some_name")
    recipe_2 = Recipe(name="some_other_name")
    recipe_3 = Recipe(name="yet_another_name")
    return [recipe_1, recipe_2, recipe_3]


class TestFoodPlan:

    def _minimal_populate_database(self, test_db, shopping_list_week_indices):
        self.shopping_list = ShoppingList(name="some_name",
                                          id=get_random_int(3))
        self.weeks = []
        self.shopping_list_weeks = []
        for n, week_index in enumerate(shopping_list_week_indices):
            self.weeks.append(Week(
                id=get_random_int(3),
                number=week_index)
            )
            self.shopping_list_weeks.append(
                ShoppingListWeek(
                    shopping_list_id=self.shopping_list.id,
                    week_id=self.weeks[n].id)
            )
        self.location = Location(session=test_db,
                                 name="some_location",
                                 id=get_random_int(3),
                                 order_id=get_random_int(3))
        self.section = Section(name="some_section",
                               location_id=self.location.id,
                               order_id=1,
                               id=get_random_int(3))
        self.shopping_list_location = ShoppingListLocation(
            shopping_list_id=self.shopping_list.id,
            location_id=self.location.id
        )
        self.recipe = Recipe(id=get_random_int(3), name="some_name")
        self.ingredient = Ingredient(id=get_random_int(3),
                                     name="some_ingredient",
                                     location_id=self.location.id,
                                     section_id=self.section.id)
        self.recipe_ingredient = RecipeIngredient(
            recipe_id=self.recipe.id,
            ingredient_id=self.ingredient.id)

        test_db.add_all(
            [self.ingredient,
             self.location,
             self.recipe,
             self.recipe_ingredient,
             self.section,
             self.shopping_list,
             self.shopping_list_location,
             *self.shopping_list_weeks,
             *self.weeks]
        )
        test_db.commit()

    def test_get_shopping_lists(self):
        shopping_list_1 = ShoppingList(name="some_name")
        shopping_list_2 = ShoppingList(name="some_other_name")
        shopping_list_3 = ShoppingList(name="yet_another_name")
        food_plan = FoodPlan([shopping_list_1,
                             shopping_list_2,
                             shopping_list_3])

        amount_shopping_lists = len(food_plan.get_shopping_lists())

        assert amount_shopping_lists == 3

    def test_set_empty_recipes_list(self):
        shopping_list = ShoppingList(name="some_name")

        food_plan = FoodPlan([shopping_list])
        food_plan.set_shopping_lists([])

        assert len(food_plan.recipes) == 0

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

    def test_add_recipe_ingredients(self, test_db):
        shopping_list_week = 1
        shopping_list_item_index = shopping_list_week - 1
        self._minimal_populate_database(
            test_db.session,
            shopping_list_week_indices=[shopping_list_week]
        )
        food_plan = FoodPlan(shopping_lists=[self.shopping_list])

        self.recipe.select(week=shopping_list_week)
        i = test_db.session.query(Ingredient).filter_by(
            location_id=self.location.id).first()
        food_plan.set_shopping_lists(recipes=[self.recipe])

        ingredients = test_db.session.query(Ingredient).filter_by(
            location_id=self.location.id,
            section_id=self.section.id
        ).first()
        assert (ingredients.shopping_list_items[shopping_list_item_index]
                is not None)
