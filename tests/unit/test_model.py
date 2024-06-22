
# Third-party imports
import pytest

# Intra-package imports
from hotshopper import (
    get_app,
    hotshopper,
    model
)
from hotshopper.errors import (
    DuplicateRecipeIngredientError,
    DuplicateRecipeError
)
from hotshopper.model import (
    Recipe,
    RecipeIngredient,
    Unit
)


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
        i = model.Ingredient(id=1, name="TestIngredient")
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
