import tkinter as tk
from tkinter.ttk import Style

from hotshopper.ingredients import kilogram, piece
# from hotshopper.hotshopper import Controller


class View(tk.Tk):
    controller = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Hotshopper")
        self.configure(background="#444")
        # self.master = tk.Tk()
        # self.master.title("Hotshopper")
        # self.master.configure(background="#444")
        # self.master = master
        # self.controller = controller
        self._frame = None
        # self.switch_frame(RecipeSelection(self.master, self.controller))

    def intialize(self, controller):
        self.controller = controller
        # self.switch_frame(RecipeSelection)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self, self.controller)
        if self._frame is not None:
            # self.grid_forget()
            # self.pack_forget()
            self._frame.destroy()
        self._frame = new_frame
        return self._frame


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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        Style().configure("Hotshopper", background="#444")

        # all_recipes = []
        self.recipes = controller.get_recipes()
        # recipes = rc.Recipe.__subclasses__()
        # selected_recipes = []
        # food_plan = FoodPlan()

        current_row = 1

        # for i in range(len(self.recipes)):
        #     all_recipes.append(self.recipes[i]())

        for recipe in self.recipes:
            checkbutton = RecipeCheckbutton(self.parent, recipe)
            checkbutton.get().grid(row=current_row, sticky="w")
            current_row += 1

        tk.Button(self.parent,
                  text="Zutaten auflisten",
                  fg="black",
                  highlightbackground='#AAA',
                  command=lambda: controller.create_shopping_list()
                  # command=lambda: parent.switch_frame(ShoppingList)
                  ).grid(row=current_row + 1)


class ShoppingList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

    def display(self):
        ingredients = self.controller.get_ingredients()

        # TODO: Since UI is not working, printing in console
        for ingredient in ingredients:
            if ingredient.unit == kilogram:
                print(f"{ingredient.amount} {ingredient.name}")
            if ingredient.unit == piece:
                print(f"{int(ingredient.amount.num)} {ingredient.name}")
            else:
                print(f"{int(ingredient.amount.num)} "
                        f"{ingredient.amount.unit} "
                        f"{ingredient.name}")

        # current_row = 0
        # for ingredient in ingredients:
        #     var = tk.StringVar()
        #     var.set(f"{ingredient.amount} {ingredient.name}")
        #     label = tk.Label(self.parent,
        #                      textvariable=var)
        #     label.configure(state="disabled", background="#444")
        #     label.grid(column=1, row=current_row, sticky="w")
        #     self.parent.update()
        #     current_row += 1
