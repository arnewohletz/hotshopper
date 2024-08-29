
# Third-party imports
import pytest
from unittest import mock

# Intra-package imports
from hotshopper import (
    get_app,
    hotshopper,
    model
)
from hotshopper.errors import (
    DuplicateIngredientError,
    DuplicateRecipeIngredientError,
    DuplicateRecipeError
)
from hotshopper.model import (
    Location,
    Recipe,
    RecipeIngredient,
    Unit
)
from tests.unit.helper import get_random_int, get_random_string


@pytest.fixture
def app():
    return get_app()


class TestController:

    def test_get_recipe(self, test_db):
        controller = hotshopper.Controller(test_db)
        r1 = model.Recipe(id=1, name="TestRecipe1")
        r2 = model.Recipe(id=2, name="TestRecipe2")
        r3 = model.Recipe(id=3, name="TestRecipe3")
        r1.add(test_db.session)
        r2.add(test_db.session)
        r3.add(test_db.session)
        r1.delete(test_db.session)
        test_db.session.commit()
        recipes = controller.get_recipes()
        assert len(recipes) == 2
        assert recipes[0].name in ["TestRecipe2", "TestRecipe3"]
        assert recipes[1].name in ["TestRecipe2", "TestRecipe3"]


class TestIngredient:

    def _minimal_populate_database(self, test_db):
        self.ingredient = model.Ingredient(
            id=get_random_int(3),
            name=get_random_string(10))
        self.recipe = model.Recipe(id=get_random_int(3),
                                   name=get_random_string(10))
        self.recipe_ingredient = model.RecipeIngredient(
            ingredient_id=self.ingredient.id,
            recipe_id=self.recipe.id)
        self.recipe.add_ingredient(self.recipe_ingredient, test_db.session)
        self.ingredient.add(test_db.session)
        test_db.session.add_all([self.ingredient,
                                 self.recipe,
                                 self.recipe_ingredient])
        test_db.session.commit()

    def test_add_new_ingredient(self, test_db):
        i = model.Ingredient(id=1, name="Ingredient")
        i.add(test_db.session)
        existing_i = test_db.session.query(
            model.Ingredient).filter_by(name="Ingredient").first()
        assert existing_i is not None
        assert i.name == existing_i.name

    def test_attempt_add_already_existing_ingredient(self, test_db):
        i_1 = model.Ingredient(id=1, name="some_ingredient")
        i_1.add(test_db.session)
        with pytest.raises(DuplicateIngredientError):
            i_1.add(test_db.session)

    def test_update_order_id(self, test_db):
        i_1 = model.Ingredient(id=1, name="ingredient_1", order_id=1)

        new_order_id = 2
        i_1.update_order_id(new_order_id, test_db.session)

        assert i_1.order_id == new_order_id

    def test_delete_existing_ingredient(self, test_db):
        self._minimal_populate_database(test_db)

        self.ingredient.delete(test_db.session)

        ingredient = test_db.session.query(model.Ingredient).first()
        recipe = test_db.session.query(
            model.Recipe).filter_by(name=self.recipe.name).first()
        assert ingredient is None
        assert recipe.ingredients == []

    def test_ingredient_is_used_by_recipe(self, test_db):
        self._minimal_populate_database(test_db)

        used_by_recipe_names = self.ingredient.used_by(test_db.session)

        assert self.recipe.name == used_by_recipe_names[0]

    def test_ingredient_not_used_by_any_recipe(self, test_db):
        ingredient = model.Ingredient(id=get_random_int(3),
                                      name="some_ingredient")
        recipe = model.Recipe(id=get_random_int(3), name="some_recipe")
        test_db.session.add_all([ingredient, recipe])
        test_db.session.commit()

        used_by_recipe_names = ingredient.used_by(test_db.session)

        assert used_by_recipe_names == []


class TestLocation:

    def test_init(self, test_db):
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(3), id=get_random_int(3))
        s = model.Section(name=get_random_string(10),
                          order_id=get_random_int(3), location_id=l.id)
        test_db.session.add_all([l, s])
        test_db.session.commit()

        l_with_s = model.Location(test_db.session, name=l.name,
                                  order_id=l.order_id, id=l.id)
        assert s.id == l_with_s.sections[0].id

    def test_section_is_appended(self, test_db):
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(3))
        test_db.session.add(l)
        test_db.session.commit()

        s = model.Section(name=get_random_string(10),
                          order_id=get_random_int(3), location_id=l.id)
        test_db.session.add(s)
        test_db.session.commit()

        l_added = test_db.session.query(Location).filter_by(
            id=l.id).first()
        assert s in l_added.sections

    def test_update_order_id(self, test_db):
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(3))
        test_db.session.add(l)

        new_order_id = str(get_random_int(10))
        l.update_order_id(new_order_id, test_db.session)

        l_updated = test_db.session.query(Location).filter_by(name=l.name).first()
        assert l_updated.order_id == new_order_id

    def test_location_has_shopping_list_item(self, test_db):
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(3))
        with mock.patch("hotshopper.model.Section") as SectionMock:
            s = SectionMock(location_id=l.id)
            s.has_shopping_list_items.return_value = True

            l.sections = [s]
            assert l.has_shopping_list_items(1) is True

    def test_location_has_no_shopping_list_item(self, test_db):
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(3))
        with mock.patch("hotshopper.model.Section") as SectionMock:
            s = SectionMock(location_id=l.id)
            s.has_shopping_list_items.return_value = False

            l.sections = [s]
            assert l.has_shopping_list_items(1) is False

    def test_location_has_shopping_list_item_no_mocks(self, test_db):
        """
        Maybe remove this test.
        """
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(1))
        s = model.Section(name=get_random_string(10),
                          order_id=get_random_int(1), location=l)
        i = model.Ingredient(name=get_random_string(10),
                             always_on_list=1, section_id=s.id)
        s.ingredients = [i]
        test_db.session.add_all([l, s, i])
        assert l.has_shopping_list_items(1) is True


    def test_location_does_not_have_shopping_list_item_no_mocks(self, test_db):
        """
        Maybe remove this test.
        """
        l = model.Location(test_db.session, name=get_random_string(10),
                           order_id=get_random_int(1))
        s = model.Section(name=get_random_string(10),
                          order_id=get_random_int(1), location=l)
        i = model.Ingredient(name=get_random_string(10),
                             always_on_list=0, section_id=s.id)
        s.ingredients = [i]
        test_db.session.add_all([l, s, i])
        assert l.has_shopping_list_items(1) is False


class TestRecipe:
    # INCOMING COMMANDS

    def test_add_new_recipe(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        r.add(test_db.session)
        r_added = test_db.session.query(Recipe).filter_by(
            name="TestRecipe").first()
        assert r.name == r_added.name

    def test_add_duplicate_recipe(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        r.add(test_db.session)
        r2 = model.Recipe(id=2, name="TestRecipe")
        with pytest.raises(DuplicateRecipeError):
            r2.add(test_db.session)

    def test_recipe_select(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        r.select(week=1)
        r.select(week=3)
        selected_weeks = [1, 3]
        assert r.selected
        assert r.weeks == selected_weeks

    def test_recipe_unselect(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        r.select(1)
        r.unselect(1)
        assert r.weeks == []
        assert not r.selected

    def test_add_ingredient_to_recipe(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        test_db.session.add(r)
        test_db.session.commit()
        result = test_db.session.query(RecipeIngredient).all()
        assert len(result) == 0
        i = model.Ingredient(id=1, name="∞")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit=Unit.GRAM)
        r.add_ingredient(ri, test_db.session)
        test_db.session.commit()
        result = test_db.session.query(RecipeIngredient).filter_by(
            ingredient_id=1).all()
        assert len(result) == 1

        with pytest.raises(DuplicateRecipeIngredientError):
            r.add_ingredient(ri, test_db.session)

    def test_remove_ingredient(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit=Unit.GRAM)
        r.add_ingredient(ri, test_db.session)
        ri.delete(test_db.session)
        result = test_db.session.query(RecipeIngredient).filter_by(
            ingredient_id=1).all()
        assert len(result) == 0

    def test_delete_recipe(self, test_db):
        r = model.Recipe(id=1, name="TestRecipeA")
        ri = model.RecipeIngredient(recipe_id=r.id, ingredient_id=1,
                                    unit=Unit.GRAM)
        ri_2 = model.RecipeIngredient(recipe_id=1000, ingredient_id=1,
                                      unit=Unit.GRAM)
        test_db.session.add(r)
        test_db.session.add(ri)
        test_db.session.add(ri_2)
        test_db.session.commit()

        assert len(test_db.session.query(Recipe).all()) == 1
        assert len(test_db.session.query(RecipeIngredient).all()) == 2

        r.delete(test_db.session)

        remain_recipe = test_db.session.query(Recipe).all()
        remain_recipe_ingredients = test_db.session.query(
            RecipeIngredient).all()

        assert len(remain_recipe) == 0
        assert len(remain_recipe_ingredients) == 1


class TestRecipeIngredient:

    def test_change_ingredient_quantity_per_person(self, test_db):
        r = model.Recipe(id=1, name="TestRecipe")
        test_db.session.add(r)
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit=Unit.GRAM)
        r.add_ingredient(ri, test_db.session)
        ri.update(test_db.session, quantity_per_person=2, unit=Unit.PIECE)
        result = test_db.session.query(RecipeIngredient).filter_by(
            ingredient_id=1).first()
        assert result.quantity_per_person == 2
        assert result.unit == Unit.PIECE

        illegal_quantities = ["100", -100, 1000000, 0]

        for value in illegal_quantities:
            with pytest.raises(ValueError):
                ri.update(test_db.session, quantity_per_person=value)
