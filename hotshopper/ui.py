import tkinter as tk
from tkinter.ttk import Style

from hotshopper.ingredients import kilogram, piece


class View(tk.Tk):

    def __init__(self):
        super(View, self).__init__()
        self.title("Hotshopper")
        self.configure(background="#444")
        self.frm_recipes = None
        self.frm_shopping_list = None
        self.foodplan = None

    def initialize(self, recipes, foodplan):
        self.foodplan = foodplan
        self.frm_recipes = RecipeSelection(self, recipes, foodplan)
        self.frm_recipes.grid(column=0, row=0)

        #TODO:
        # Have to move logic to Controller here
        # Have to differentiate between frame recipeSelection & shopping list

        # self.switch_frame(RecipeSelection(self, recipes, foodplan))

        # def update_frame(self, new_frame):

    #     if type(new_frame) in self._frames:
    #         pass

    def switch_frame(self, frame_class):
        new_frame = frame_class
        if type(self._frame) == type(frame_class):
            # self.grid_forget()
            # self.pack_forget()
            for widget in self._frame.winfo_children():
                widget.destroy()
            self._frame.grid_forget()
        self._frame = new_frame
        self._frame.grid()


class RecipeCheckbutton:

    def __init__(self, master, recipe):
        self.recipe = recipe
        self.selected = tk.BooleanVar()
        self.button = tk.Checkbutton(master,
                                     text=self.recipe.name,
                                     variable=self.selected,
                                     onvalue=True,
                                     offvalue=False,
                                     command=self.set_selected,
                                     bg="#444",
                                     fg="white")
        # self.button.pack()

    def set_selected(self):
        self.recipe.set_selected(self.recipe, self.selected)

    def get(self):
        return self.button


class RecipeSelection(tk.Frame):

    def __init__(self, master, recipes, foodplan):
        tk.Frame.__init__(self, master)
        self.master = master
        self.recipes = recipes
        self.foodplan = foodplan
        # Style().configure("Hotshopper", background="#444")

        # all_recipes = []
        # self.recipes = controller.get_recipes()
        # recipes = rc.Recipe.__subclasses__()
        # selected_recipes = []
        # food_plan = FoodPlan()

        current_row = 0

        for recipe in self.recipes:
            checkbutton = RecipeCheckbutton(self.master, recipe)
            checkbutton.get().grid(row=current_row, sticky="w")
            current_row += 1

        tk.Button(self.master,
                  text="Zutaten auflisten",
                  fg="black",
                  highlightbackground='#AAA',
                  # command=lambda: master.switch_frame(
                  #     ShoppingList(master, self.get_shopping_list())),
                  command=lambda: master.switch_frame(
                      ShoppingList(master, self.get_shopping_list()))
                  ).grid(row=current_row + 1)

    def get_shopping_list(self):
        self.foodplan.set_shopping_list(self.recipes)
        return self.foodplan.get_shopping_list()


class ShoppingList(tk.Frame):

    def __init__(self, master, ingredients):
        tk.Frame.__init__(self, master)
        self.master = master
        self.ingredients = ingredients

        current_row = 0
        for ingredient in self.ingredients:
            var = tk.StringVar()
            if ingredient.amount.num > 0.0 and ingredient.amount_piece.num == 0:
                var.set(f"{ingredient.amount} {ingredient.name}")
            elif ingredient.amount.num == 0.0 and ingredient.amount_piece.num >= 0:
                var.set(f"{ingredient.amount_piece} {ingredient.name}")
            else:
                var.set(f"{ingredient.amount} + {ingredient.amount_piece} "
                        f"{ingredient.name}")
            label = tk.Label(self.master,
                             textvariable=var)
            label.configure(state="disabled", background="#444")
            label.grid(column=1, row=current_row, sticky="w")
            current_row += 1

    # def initialize(self):
    #     current_row = 0
    #     for ingredient in self.ingredients:
    #         var = tk.StringVar()
    #         var.set(f"{ingredient.amount} {ingredient.name}")
    #         label = tk.Label(self.parent,
    #                          textvariable=var)
    #         label.configure(state="disabled", background="#444")
    #         label.grid(column=1, row=current_row, sticky="w")
    #         current_row += 1
    #     return label

    # def display(self):
    # ingredients = self.controller.get_ingredients()

    # TODO: Since UI is not working, printing in console
    # for ingredient in ingredients:
    #     if ingredient.unit == kilogram:
    #         print(f"{ingredient.amount} {ingredient.name}")
    #     if ingredient.unit == piece:
    #         print(f"{int(ingredient.amount.num)} {ingredient.name}")
    #     else:
    #         print(f"{int(ingredient.amount.num)} "
    #               f"{ingredient.amount.unit} "
    #               f"{ingredient.name}")

    # current_row = 0
    # for ingredient in self.ingredients:
    #     var = tk.StringVar()
    #     var.set(f"{ingredient.amount} {ingredient.name}")
    #     label = tk.Label(self.parent,
    #                      textvariable=var)
    #     label.configure(state="disabled", background="#444")
    #     label.grid(column=1, row=current_row, sticky="w")
    #     self.parent.update()
    #     current_row += 1
