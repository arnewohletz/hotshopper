from abc import ABC
from units import unit
from hotshopper.errors import UnsupportedUnitError

piece = unit("St.")
gram = unit("g")
kilogram = unit("kg")


class Ingredient(ABC):
    amount_weight = None
    amount_piece = None
    name = ""

    def __init__(self, unit: unit, amount: int):
        self.unit = unit
        if unit not in (piece, gram, kilogram):
            raise UnsupportedUnitError("This unit is not supported")
        if unit == piece:
            self.amount_piece = unit(amount)
        else:
            self.amount_weight = unit(amount)


class Carrot(Ingredient):
    name = "Kartotten"


class Onion(Ingredient):
    name = "Zwiebeln"


class Potato(Ingredient):
    pass


class LowStarchPotatoe(Potato):
    name = "Kartoffeln festk."


class StarchyPotato(Potato):
    name = "Kartoffeln mehlig"


class PrimarilyWaxyPotato(Potato):
    name = "Kartoffeln vorw. festk."
