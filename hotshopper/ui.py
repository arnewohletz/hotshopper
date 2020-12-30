import tkinter as tk


class View(tk.Tk):

    def __init__(self):
        super(View, self).__init__()
        self.title("Hotshopper")
        self.configure(background="#444")
        self.frm_recipes = None
        self.frm_shopping_list = None
        self.foodplan = None
        self.frames = []

    def initialize(self, recipes, foodplan):
        self.foodplan = foodplan
        frm_recipes = RecipeSelection(self, recipes, foodplan)
        frm_recipes.grid(column=0, row=0)
        self.frames.append(frm_recipes)

    def add_frame(self, frame):
        self.frames.append(frame)
        return frame

    def update_frame(self, frame):

        for f in self.frames:
            if isinstance(f, type(frame)):
                f.grid_forget()
                self.frames.remove(f)
                f.destroy()
                return frame

        self.add_frame(frame)
        return frame


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

        current_row = 0

        for recipe in self.recipes:
            checkbutton = RecipeCheckbutton(self.master, recipe)
            checkbutton.get().grid(row=current_row, sticky="w")
            current_row += 1

        tk.Button(self.master,
                  text="Zutaten auflisten",
                  fg="black",
                  highlightbackground='#AAA',
                  command=lambda: master.update_frame(
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

