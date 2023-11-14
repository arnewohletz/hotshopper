import random
import string

from hotshopper.model import Recipe, Ingredient, RecipeIngredient


def get_random_string(length: int):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class TestDataGenerator:

    def __init__(self, db):
        self.db = db
        self.next_recipe_id = 0
        self.next_ingredient_id = 0

    def create_recipe(self):
        r = Recipe(name=get_random_string(10), ingredients=[])
        self.next_recipe_id += 1
        self.db.session.add(r)

        return r.id

    def create_ingredient(self, where, name=None):
        if not name:
            name = get_random_string(10)
        i = Ingredient(id=self.next_ingredient_id, name=name,
                       order_id=random.randint(1,10000), location_id=where)
        self.db.session.add(i)
        self.next_ingredient_id += 1

        return i.id

    def create_recipe_ingredient(self, recipe_id, ingredient_id,
                                 quantity_per_person=100, unit="gram"):
        ri = RecipeIngredient(recipe_id=recipe_id,
                              ingredient_id=ingredient_id,
                              quantity_per_person=quantity_per_person,
                              unit=unit)
        self.db.session.add(ri)
        return None

    def get_recipe(self, recipe_id):
        return self.db.session.query(Recipe).filter_by(id=recipe_id).first()
