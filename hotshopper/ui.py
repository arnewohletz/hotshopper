import tkinter as tk
from tkinter import ttk

BACKGROUND_COLOR: str = "#444"


class View(tk.Tk):
    def __init__(self):
        super(View, self).__init__()
        self.title("Hotshopper")
        self.configure(background=BACKGROUND_COLOR)
        self.geometry("900x800")
        self.controller = None
        self.frm_recipes = None
        self.frm_shopping_lists = None

    def initialize(self, controller, recipes):
        self.controller = controller
        self.frm_recipes = RecipeSelection(self, recipes)
        self.frm_recipes.grid(row=0, column=0, sticky="nw")

    def display_shopping_lists(self, shopping_lists):
        self.frm_shopping_lists = None
        frm_shopping_lists = ShoppingListsFrame(self, shopping_lists)
        frm_shopping_lists.grid(column=1, row=0, sticky="nw")
        frm_shopping_lists.add_shopping_list_frames()
        frm_shopping_lists.update_scroll_region()


class RecipeCheckbutton:
    def __init__(self, master, recipe, week):
        self.recipe = recipe
        self.week = week
        self.selected = tk.BooleanVar()
        self.button = tk.Checkbutton(
            master,
            variable=self.selected,
            onvalue=True,
            offvalue=False,
            command=self.set_selected,
            bg=BACKGROUND_COLOR,
            fg="white",
        )

    def set_selected(self):
        self.recipe.select(self.selected.get(), self.week)

    def get(self):
        return self.button


class RecipeSelection(tk.Frame):
    def __init__(self, master, recipes):
        tk.Frame.__init__(self, master, bg=BACKGROUND_COLOR, padx=10)
        self.master = master
        self.recipes = recipes

        # create and position frames
        self.frame_header = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.frame_canvas = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.canvas_recipes = tk.Canvas(
            self.frame_canvas,
            width=500,
            height=700,
            bg=BACKGROUND_COLOR,
            scrollregion=(0, 0, 0, 800),
        )
        self.frame_buttons = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.frame_recipes = tk.Frame(self.canvas_recipes, bg=BACKGROUND_COLOR,
                                      padx=3)

        self.frame_header.grid(row=0, column=0, sticky="w")
        self.frame_canvas.grid(row=1, column=0, sticky="w")
        self.canvas_recipes.grid(row=0, column=0, sticky="ew")
        self.frame_buttons.grid(row=2, column=0, sticky="ew")

        # add content to frames
        self.fill_header()
        self.fill_recipes()
        self.add_buttons()

        self.update_scroll_region()

        # add scrollbar for recipes
        self.vsb = ttk.Scrollbar(
            self.frame_canvas, orient="vertical",
            command=self.canvas_recipes.yview
        )
        self.vsb.grid(row=0, column=4, sticky="ns")

        self.canvas_recipes.create_window(
            (0, 0), width=500, window=self.frame_recipes, anchor="nw"
        )
        self.canvas_recipes.config(yscrollcommand=self.vsb.set)

    def fill_header(self):
        current_row = 0
        frame = self.frame_header

        tk.Label(frame, text="Woche", bg=BACKGROUND_COLOR, fg="white").grid(
            row=current_row, column=0, columnspan=4, sticky="ew"
        )
        current_row += 1

        tk.Label(frame, text="1", bg=BACKGROUND_COLOR, fg="white",
                 padx=5).grid(row=current_row, column=0, sticky="ew"
                              )
        tk.Label(frame, text="2", bg=BACKGROUND_COLOR, fg="white",
                 padx=5).grid(row=current_row, column=1, sticky="ew"
                              )
        tk.Label(frame, text="3", bg=BACKGROUND_COLOR, fg="white",
                 padx=5).grid(row=current_row, column=2, sticky="ew"
                              )

    def fill_recipes(self):
        current_row = 0
        frame = self.frame_recipes

        for recipe in self.recipes:
            checkbutton_week1 = RecipeCheckbutton(frame, recipe, 1)
            checkbutton_week2 = RecipeCheckbutton(frame, recipe, 2)
            checkbutton_week3 = RecipeCheckbutton(frame, recipe, 3)
            checkbutton_week1.get().grid(row=current_row, column=0, sticky="w")
            checkbutton_week2.get().grid(row=current_row, column=1, sticky="w")
            checkbutton_week3.get().grid(row=current_row, column=2, sticky="w")
            tk.Label(frame, text=recipe.name, bg=BACKGROUND_COLOR,
                     fg="white").grid(
                row=current_row, column=3, sticky="w"
            )
            current_row += 1

    def add_buttons(self):
        frame = self.frame_buttons

        tk.Button(
            frame,
            text="Einkaufsliste erstellen",
            fg="black",
            relief="raised",
            padx=3,
            pady=3,
            highlightbackground="#444",
            command=lambda: self.master.controller.display_shopping_lists(),
        ).grid(row=0, columnspan=4)

    def _on_mousewheel(self, event):
        self.canvas_recipes.yview_scroll(int(-1 * event.delta), "units")

    def update_scroll_region(self):
        self.canvas_recipes.update_idletasks()
        self.canvas_recipes.config(scrollregion=self.frame_recipes.bbox())
        self.canvas_recipes.bind_all("<MouseWheel>", self._on_mousewheel)


class ShoppingListsFrame(tk.Frame):
    def __init__(self, master, shopping_lists: list):
        """
        :param shopping_lists: A list of ShoppingList objects
        """
        tk.Frame.__init__(
            self,
            master,
            bg=BACKGROUND_COLOR,
        )
        self.master = master
        self.shopping_lists = shopping_lists
        self.canvas_shopping_lists = tk.Canvas(
            self,
            width=300,
            height=950,
            bg=BACKGROUND_COLOR,
            scrollregion=(0, 0, 0, 800),
        )
        self.frame_shopping_lists = tk.Frame(
            self.canvas_shopping_lists, bg=BACKGROUND_COLOR
        )
        self.canvas_shopping_lists.create_window(
            (0, 0), width=300, window=self.frame_shopping_lists, anchor="nw"
        )
        self.vsb = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas_shopping_lists.yview
        )
        self.canvas_shopping_lists.grid(row=0, column=0, sticky="nw")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.canvas_shopping_lists.config(yscrollcommand=self.vsb.set)

    def add_shopping_list_frames(self):
        current_row = 0

        for shopping_list in self.shopping_lists:
            frame = ShoppingListFrame(self.frame_shopping_lists, shopping_list)
            frame.grid(column=0, row=current_row, sticky="w")
            current_row += 1
            frame.add_ingredients()

    def _on_mousewheel(self, event):
        self.canvas_shopping_lists.yview_scroll(int(-1 * event.delta), "units")

    def update_scroll_region(self):
        self.canvas_shopping_lists.update_idletasks()
        self.canvas_shopping_lists.config(
            scrollregion=self.frame_shopping_lists.bbox())
        self.canvas_shopping_lists.bind_all("<MouseWheel>",
                                            self._on_mousewheel)


class ShoppingListFrame(tk.Frame):
    def __init__(self, master, shopping_list):
        tk.Frame.__init__(self, master, bg=BACKGROUND_COLOR)
        self.master = master
        self.shopping_list = shopping_list

    def add_ingredients(self):
        current_row = 0
        tk.Label(self, text=self.shopping_list.get_name(), bg="#FFF",
                 fg="black").grid(
            row=current_row, column=0, sticky="nw"
        )
        current_row += 1

        for ingredient in self.shopping_list:
            var = tk.StringVar()
            if ingredient.amount_gram.num > 0.0:
                if ingredient.amount_piece.num == 0:
                    var.set(f"{ingredient.amount_gram} {ingredient.name}")
            elif ingredient.amount_gram.num == 0.0:
                if ingredient.amount_piece.num >= 0:
                    var.set(f"{ingredient.amount_piece} {ingredient.name}")
            else:
                var.set(
                    f"{ingredient.amount_gram} + {ingredient.amount_piece} "
                    f"{ingredient.name}"
                )
            label = tk.Label(
                self, textvariable=var, state="disabled", bg=BACKGROUND_COLOR
            )
            label.grid(column=0, row=current_row, sticky="nw")
            current_row += 1
