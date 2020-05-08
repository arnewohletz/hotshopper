from abc import ABC

from hotshopper.ingredients import Carrot, Onion
from hotshopper.ingredients import gram, piece


class Recipe(ABC):
    name = ""
    ingredients = []

    def print_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient.amount_piece:
                print(f"{ingredient.amount_piece.num} {ingredient.name}")
            else:
                print(f"{ingredient.amount_weight} {ingredient.name}")


class PotatoSoup(Recipe):
    name = "Kartoffelsuppe"
    ingredients = [Carrot(gram, 500),
                   Onion(piece, 1),
                   ]
