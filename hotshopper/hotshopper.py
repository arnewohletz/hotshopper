"""Main module."""
import tkinter as tk
from tkinter.ttk import Style
import hotshopper.recipes as rc


class RecipeCheckbutton:

    def __init__(self, parent, recipe):
        selected = tk.BooleanVar()
        self.button = tk.Checkbutton(parent,
                                     text=recipe.name,
                                     variable=selected,
                                     onvalue=True,
                                     offvalue=False,
                                     command=lambda: recipe.set_selected(
                                         selected),
                                     bg="#444",
                                     fg="white")

    def get(self):
        return self.button


class RecipeSelection(tk.Frame):

    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.parent = parent
        Style().configure("Hotshopper", background="#444")

        all_recipes = []
        recipes = rc.Recipe.__subclasses__()
        selected_recipes = {}

        current_row = 1

        for i in range(len(recipes)):
            all_recipes.append(recipes[i]())

        for recipe in all_recipes:
            checkbutton = RecipeCheckbutton(self.parent, recipe)
            checkbutton.get().grid(row=current_row, sticky="w")
            current_row += 1

        tk.Button(self.parent,
                  text="Zutaten auflisten",
                  fg="black",
                  highlightbackground='#AAA',
                  command="calculate").grid(row=current_row + 1)


def main():
    root = tk.Tk()
    root.title("Hotshopper")
    root.configure(background="#444")
    RecipeSelection(root)
    root.mainloop()
