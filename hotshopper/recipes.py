from abc import ABC

from hotshopper.ingredients import Carrot, Onion, LowStarchPotatoe, ChiliPepper
from hotshopper.ingredients import gram, piece


class Recipe(ABC):
    name = ""
    ingredients = []


class PotatoSoup(Recipe):
    name = "Kartoffelsuppe"
    ingredients = [Carrot(gram, 500),
                   Onion(piece, 1),
                   ]


class ParsleyRootCurry(Recipe):
    name = "Petersilienwurzelcurry"
    ingredients = [LowStarchPotatoe(gram, 750),
                   ChiliPepper(piece, 1),
                   Carrot(gram, 250),
                   ]
