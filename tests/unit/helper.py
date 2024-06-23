
# Standard library imports
import math
import random
import string

# Intra-package imports
from hotshopper.model import (
    Ingredient,
    Location,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Week
)


def get_random_string(length: int):
    """Return a random ASCII string of the defined length"""
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_random_int(length: int):
    """Return a random integer of the defined length"""
    minimum = int(math.pow(10, length - 1))
    maximum = int(math.pow(10, length) - 1)
    return random.randint(minimum, maximum)


class RandomTestDataGenerator:
    def __init__(self, db):
        self.db = db
        self.next_recipe_id = 0
        self.next_ingredient_id = 0

    def create_recipe(self):
        r = Recipe(name=get_random_string(10), ingredients=[])
        self.next_recipe_id += 1
        self.db.session.add(r)

        return r

    # def create_shopping_list(self):
    #     return ShoppingList(name="some_name")
    #     # s = ShoppingList(name="some_name",
    #     #     locations=[Location(name="some_location", order_id=1,
    #     #                         session=self.db.session)],
    #     #     weeks = [Week(number=1)],
    #     #     print_columns = 1)
    #     # return s

    def create_ingredient(self, where, name=None):
        if not name:
            name = get_random_string(10)
        i = Ingredient(id=self.next_ingredient_id, name=name,
                       order_id=random.randint(1,10000), location_id=where)
        self.db.session.add(i)
        self.next_ingredient_id += 1

        return i.id

    def create_recipe_ingredient(self,
                                 recipe_id=get_random_int(3),
                                 ingredient_id=get_random_int(3),
                                 quantity_per_person=get_random_int(3),
                                 unit="gram"):
        ri = RecipeIngredient(recipe_id=recipe_id,
                              ingredient_id=ingredient_id,
                              quantity_per_person=quantity_per_person,
                              unit=unit)
        # self.db.session.add(ri)
        return ri

    def get_recipe(self, recipe_id):
        return self.db.session.query(Recipe).filter_by(id=recipe_id).first()
