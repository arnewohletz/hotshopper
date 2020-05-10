from abc import ABC
from units import unit, scaled_unit
from hotshopper.errors import UnsupportedUnitError

piece = unit("St.")
gram = unit("g")
kilogram = scaled_unit("kg", "gram", 1000)


class Ingredient(ABC):
    name = ""

    def __init__(self, unit: unit, amount: int):
        self.unit = unit
        if unit not in (piece, gram, kilogram):
            raise UnsupportedUnitError("This unit is not supported")
        self.amount = unit(amount)


class ChiliPepper(Ingredient):
    name = "Chilischote"


class Carrot(Ingredient):
    name = "Karotten"


class Onion(Ingredient):
    name = "Zwiebeln"


class _Potato(Ingredient):
    pass


class LowStarchPotatoe(_Potato):
    name = "Kartoffeln festk."


class StarchyPotato(_Potato):
    name = "Kartoffeln mehlig"


class PrimarilyWaxyPotato(_Potato):
    name = "Kartoffeln vorw. festk."
