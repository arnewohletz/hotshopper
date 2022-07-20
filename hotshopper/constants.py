from dataclasses import dataclass


@dataclass
class Location:
    SUPERMARKET = "supermarket"
    MARKET = "market"


@dataclass
class Unit:
    PIECE = "st."
    GRAM = "g"
