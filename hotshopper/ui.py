import tkinter as tk


class View(tk.Tk):

    def __init__(self):
        super(View, self).__init__()
        self.title("Hotshopper")
        self.configure(background="#444")
        self.controller = None
        self.frm_recipes = None
        self.frm_shopping_lists = None
        # self.foodplan = None
        # self.frames = []

    def initialize(self, controller, recipes):
        self.controller = controller
        # self.foodplan = foodplan
        self.frm_recipes = RecipeSelection(self, recipes)
        self.frm_recipes.grid(column=0, row=0)
        # self.frames.append(frm_recipes)

    def display_shopping_lists(self, shopping_lists):
        frm_shopping_lists = ShoppingListsFrame(self, shopping_lists)
        frm_shopping_lists.grid(column=1, row=0)

    def add_frame(self, frame, row, column):
        frame.grid(column=column, row=row, sticky="nw")

    # def add_frame(self, frame):
    #     self.frames.append(frame)
    #     return frame

    # def update_frame(self, frame):
    #     for f in self.frames:
    #         if isinstance(f, type(frame)):
    #             f.grid_forget()
    #             self.frames.remove(f)
    #             f.destroy()
    #             return frame
    #
    #     self.add_frame(frame)
    #     return frame


class RecipeCheckbutton:

    def __init__(self, master, recipe, week):
        self.recipe = recipe
        self.week = week
        self.selected = tk.BooleanVar()
        self.button = tk.Checkbutton(master,
                                     variable=self.selected,
                                     onvalue=True,
                                     offvalue=False,
                                     command=self.set_selected,
                                     bg="#444",
                                     fg="white")

    def set_selected(self):
        self.recipe.set_selected(self.recipe, self.selected, self.week)

    def get(self):
        return self.button


class RecipeSelection(tk.Frame):

    def __init__(self, master, recipes):
        tk.Frame.__init__(self, master, bg="#444")
        self.master = master
        self.recipes = recipes
        # self.foodplan = foodplan

        current_row = 0
        tk.Label(self, text="Woche", bg="#444", fg="white").grid(
            row=current_row,
            column=0,
            columnspan=3,
            sticky="ew")
        current_row += 1

        tk.Label(self, text="1", bg="#444", fg="white").grid(
            row=current_row, column=0, sticky="ew")
        tk.Label(self, text="2", bg="#444", fg="white").grid(
            row=current_row, column=1, sticky="ew")
        tk.Label(self, text="3", bg="#444", fg="white").grid(
            row=current_row, column=2, sticky="ew")

        current_row += 1

        for recipe in self.recipes:
            checkbutton_week1 = RecipeCheckbutton(self, recipe, 1)
            checkbutton_week2 = RecipeCheckbutton(self, recipe, 2)
            checkbutton_week3 = RecipeCheckbutton(self, recipe, 3)
            checkbutton_week1.get().grid(row=current_row, column=0, sticky="w")
            checkbutton_week2.get().grid(row=current_row, column=1, sticky="w")
            checkbutton_week3.get().grid(row=current_row, column=2, sticky="w")
            tk.Label(self, text=recipe.name, bg="#444", fg="white").grid(
                row=current_row, column=3, sticky="w")
            current_row += 1

        tk.Button(self.master,
                  text="Zutaten auflisten",
                  fg="black",
                  highlightbackground='#AAA',
                  command=lambda: self.master.controller.display_shopping_lists(
                      self.recipes),
                  # command=lambda: master.add_frame(
                  #     ShoppingLists(master, self.get_shopping_lists()), row=0,
                  #     column=4)
                  ).grid(row=current_row + 1, columnspan=4)

    # def get_shopping_lists(self):
    #     self.foodplan.set_shopping_lists(self.recipes)
    #     return self.foodplan.get_shopping_lists()


class ShoppingListsFrame(tk.Frame):

    def __init__(self, master, shopping_lists: list):
        """
        :param shopping_lists: A list of ShoppingList objects
        """
        tk.Frame.__init__(self, master, bg="#444")
        self.master = master
        # self.ingredients = ingredients

        current_row = 0

        for shopping_list in shopping_lists:
            frame = ShoppingListFrame(self, shopping_list)
            frame.grid(column=1, row=current_row)
            current_row += 1


class ShoppingListFrame(tk.Frame):

    def __init__(self, master, ingredients):
        tk.Frame.__init__(self, master, bg="#444")
        self.master = master
        self.ingredients = ingredients

        current_row = 0
        for ingredient in self.ingredients:
            name = tk.Label(self.master, textvariable=ingredient.name)
            name.grid(column=0, row=current_row)
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
