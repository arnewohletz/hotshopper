import pytest

from hotshopper import model, db, create_app
from hotshopper.model import RecipeIngredient
from hotshopper.errors import DuplicateRecipeIngredientError
from tests.unit import helper


@pytest.fixture
def app():
    return create_app(test=True)


# @pytest.fixture
# def db(app):
#     return SQLAlchemy(app)

@pytest.fixture(scope="function")
def setup_teardown():
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


class TestRecipe:
    # INCOMING COMMANDS

    def test_recipe_select(self):
        selected_weeks = [1, 3]
        dummy_recipe = helper.dummy_recipe(weeks=selected_weeks)
        assert dummy_recipe.selected
        assert dummy_recipe.weeks == selected_weeks

    def test_recipe_unselect(self):
        dummy_recipe = helper.dummy_recipe()
        dummy_recipe.select(1)
        dummy_recipe.unselect(1)
        assert dummy_recipe.weeks is None
        assert not dummy_recipe.selected

    def test_add_ingredient_to_recipe(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        db.session.add(r)
        result = RecipeIngredient.query.all()
        assert len(result) == 0
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit="gram")
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
                                    quantity_per_person=100, unit="gram")
        r.add_ingredient(ri)
        r.remove_ingredient(ri)
        r.save_recipe()
        result = RecipeIngredient.query.filter_by(ingredient_id=1).all()
        assert len(result) == 0


class TestRecipeIngredient:

    def test_change_ingredient_quantity_per_person(self, app, setup_teardown):
        r = model.Recipe(id=1, name="TestRecipe", ingredients=[])
        db.session.add(r)
        i = model.Ingredient(id=1, name="TestIngredient")
        ri = model.RecipeIngredient(ingredient_id=r.id, recipe_id=i.id,
                                    quantity_per_person=100, unit="gram")
        r.add_ingredient(ri)
        ri.update_quantity(quantity_per_person=2, unit="St.")
        result = RecipeIngredient.query.filter_by(ingredient_id=1).first()
        assert result.quantity_per_person == 2
        assert result.unit == "St."

        illegal_quantities = ["100", -100, 1000000, 0]

        for value in illegal_quantities:
            with pytest.raises(ValueError):
                ri.update_quantity(quantity_per_person=value)
