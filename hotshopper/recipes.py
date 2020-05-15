import tkinter as tk

from abc import ABC, ABCMeta

from hotshopper.ingredients import Carrot, Onion, LowStarchPotatoe, ChiliPepper
from hotshopper.ingredients import gram, piece


class Recipe(ABC):
    name = ""
    ingredients = []
    selected = False

    def set_selected(self, selected: tk.BooleanVar):
        if selected.get():
            self.selected = True
            print(self.name + " is selected")
        else:
            self.selected = False
            print(self.name + " is deselected")

    # def select(self):
    #     self.selected = True
    #
    # def deselect(self):
    #     self.selected = False


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
                   Onion(piece, 5)]
