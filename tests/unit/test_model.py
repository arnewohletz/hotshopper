import pytest

from hotshopper import hotshopper
from hotshopper import model, db, create_app
from hotshopper.constants import Unit
from hotshopper.errors import (
    DuplicateRecipeIngredientError,
    DuplicateRecipeError
)
from hotshopper.model import Recipe, RecipeIngredient

@pytest.fixture
def app():
    return create_app(test=True)


@pytest.fixture(scope="function")
def setup_teardown():
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


class TestController:

    def test_get_recipe(self, app, setup_teardown):
        controller = hotshopper.Controller()
        r1 = model.Recipe(id=1, name="TestRecipe1", ingredients=[])
        r2 = model.Recipe(id=2, name="TestRecipe2", ingredients=[])
        r3 = model.Recipe(id=3, name="TestRecipe3", ingredients=[])
        r1.add()
        r2.add()
        r3.add()
        r1.delete()
        db.session.commit()
        recipes = controller.get_recipes()
        assert len(recipes) == 2
        assert recipes[0].name in ["TestRecipe2", "TestRecipe3"]
        assert recipes[1].name in ["TestRecipe2", "TestRecipe3"]


class TestRecipe:
    # INCOMING COMMANDS

    def test_add_new_recipe(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        r.add()
        r_added = Recipe.query.filter_by(name="TestRecipe").first()
        assert r.name == r_added.name

    def test_add_duplicate_recipe(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        r.add()
        r2 = model.Recipe(id=2, name="TestRecipe", ingredients=[])
        with pytest.raises(DuplicateRecipeError):
            r2.add()

    def test_recipe_select(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        r.select(week=1)
        r.select(week=3)
        selected_weeks = [1, 3]
        assert r.selected
        assert r.weeks == selected_weeks

    def test_recipe_unselect(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        r.select(1)
        r.unselect(1)
        assert r.weeks is None
        assert not r.selected

    def test_add_ingredient_to_recipe(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        db.session.add(r)
        result = RecipeIngredient.query.all()
        assert len(result) == 0
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit=Unit.GRAM)
        r.add_ingredient(ri)
        db.session.commit()
        result = RecipeIngredient.query.filter_by(ingredient_id=1).all()
        assert len(result) == 1

        with pytest.raises(DuplicateRecipeIngredientError):
            r.add_ingredient(ri)

    def test_remove_ingredient(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe",
                         ingredients=[])
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit=Unit.GRAM)
        r.add_ingredient(ri)
        ri.delete()
        result = RecipeIngredient.query.filter_by(ingredient_id=1).all()
        assert len(result) == 0

    def test_delete_recipe(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipeA", ingredients=[])
        ri = model.RecipeIngredient(recipe_id=r.id, ingredient_id=1,
                                    amount=100, unit=Unit.GRAM)
        ri_2 = model.RecipeIngredient(recipe_id=1000, ingredient_id=1,
                                      amount=100, unit=Unit.GRAM)
        db.session.add(r)
        db.session.add(ri)
        db.session.add(ri_2)

        assert len(Recipe.query.all()) == 1
        assert len(RecipeIngredient.query.all()) == 2

        r.delete()

        remain_recipe = Recipe.query.all()
        remain_recipe_ingredients = RecipeIngredient.query.all()

        assert len(remain_recipe) == 0
        assert len(remain_recipe_ingredients) == 1


class TestRecipeIngredient:

    def test_change_ingredient_quantity_per_person(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        db.session.add(r)
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit=Unit.GRAM)
        r.add_ingredient(ri)
        ri.update(quantity_per_person=2, unit=Unit.PIECE)
        result = RecipeIngredient.query.filter_by(ingredient_id=1).first()
        assert result.quantity_per_person == 2
        assert result.unit == Unit.PIECE

        illegal_quantities = ["100", -100, 1000000, 0]

        for value in illegal_quantities:
            with pytest.raises(ValueError):
                ri.update(quantity_per_person=value)
