function init() {
    // document.getElementById("add_recipe_screen").style.display = "none";
    // document.getElementById("EDIT_RECIPE_screen").style.display = "none";
    // document.getElementById("cover").style.display = "none";
    // document.getElementById('add_recipe_form').reset();
    window.scroll(0, scroll_height);
}

function set_selected(checkboxElem) {
    let scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    if (checkboxElem.checked) {
        window.location.href = "/check_recipe/" + checkboxElem.id + "_" + scroll_height;
    } else {
        window.location.href = "/uncheck_recipe/" + checkboxElem.id + "_" + scroll_height;
    }
}

let amount_ingredients = 0;

function show_add_recipe_screen() {
    // new_ingredient_index = 1;
    // document.getElementById("cover").style.display = "block";
    // document.getElementById("add_recipe_screen").style.display = "block";
    window.location.href = "/add_recipe"
}

function show_add_ingredient_screen() {
    window.location.href ="/ingredients/new"
}

function show_ingredients_screen() {
    window.location.href = "/ingredients"
}

function show_shopping_list_screen() {
    window.location.href = "/shopping_list"
}

// function cancel_close_recipe_screen() {
//     document.getElementById("add_recipe_screen").style.display = "none";
//     document.getElementById("cover").style.display = "none";
//     document.getElementById('add_recipe_form').reset();
// }

function formcheck() {
    let fields = document.querySelectorAll("select, textarea, input, [required]")
    let complete = true;
    for (let field of fields) {
        if (!field.value) {
            field.style.borderColor = "red";
            complete = false;
        } else {
            field.style.borderColor = "black";
        }
        if (field.className === "quantity" && (field.value < 0.1 || field.value > 99999.9)) {
            field.style.borderColor = "red";
            complete = false;
        }
    }
    return complete;
}

function confirm_close_recipe_screen(edit = false) {
    if (!formcheck()) {
        return false;
    }
    let current_scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    let current_recipe_amount_ingredients = document.getElementsByClassName("recipe_ingredient").length;
    document.getElementById("cover").style.display = "none";
    let current_recipe_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
    const template_add = new_ingredient_index => `/confirm_new_recipe/${new_ingredient_index}_${current_scroll_height}`
    const template_edit = new_ingredient_index => `/confirm_edit_recipe/${current_recipe_id}_${new_ingredient_index}_${current_scroll_height}`

    if (edit) {
        document.getElementById("edit_recipe_screen").style.display = "none";
        document.getElementById("edit_recipe_form").addEventListener(
            "submit", function (s) {
                s.preventDefault();
                this.action = template_edit(current_recipe_amount_ingredients);
                this.submit();
            });
    } else {
        document.getElementById("add_recipe_screen").style.display = "none";
        document.getElementById("add_recipe_form").addEventListener(
            "submit", function (s) {
                s.preventDefault();
                this.action = template_add(current_recipe_amount_ingredients);
                this.submit();
            });
    }
}

function add_ingredient() {

}

function delete_recipe(recipe) {
    let scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    Swal.fire({
        text: `Rezept "${recipe.name}" wirklich löschen?`,
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: 'Abbruch',
        confirmButtonText: 'OK',
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = recipe.id + "_" + scroll_height;
        }
    })
}

function edit_recipe(recipe) {
    window.location.href = recipe.id;
}

function delete_recipe_ingredient(ingredient) {
    document.getElementById(`recipe_ingredient_${ingredient}`).remove();
}

function add_recipe_ingredient() {
    // get new ingredient index
    amount_ingredients = document.getElementById("recipe_table").getElementsByClassName("recipe_ingredient").length;


    // add new recipe ingredients nodes
    let NewRecipeTable = document.getElementById("recipe_table");
    let NewRecipeIngredientTable = document.createElement("table");
    let NewRecipeIngredientRow = document.createElement("tr");
    NewRecipeIngredientRow.setAttribute("class", "recipe_ingredient");
    NewRecipeIngredientRow.setAttribute("id", `recipe_ingredient_${amount_ingredients}`);
    let InputQuantityCell = document.createElement("td");
    let UnitCell = document.createElement("td");
    let IngredientCell = document.createElement("td");
    let DeleteButtonCell = document.createElement("td");

    // create quantity node
    let InputQuantity = document.createElement("input");
    InputQuantity.setAttribute('type', "number");
    InputQuantity.setAttribute('size', "3");
    InputQuantity.setAttribute('id', `quantity_${amount_ingredients}`);
    InputQuantity.setAttribute('name', `quantity_${amount_ingredients}`);
    InputQuantity.setAttribute('class', 'quantity');
    InputQuantity.setAttribute('min', '0.0');
    InputQuantity.setAttribute('max', '10000.0');
    InputQuantity.setAttribute('required', "");

    // get empty cell ("Zutaten:") real width
    let IngredientLabelElement = document.getElementById("label_ingredients");
    let style = window.getComputedStyle(IngredientLabelElement);
    let EmptyCellWidth = document.getElementById("label_ingredients").clientWidth - parseFloat(style.paddingLeft) -parseFloat(style.paddingRight);

    // create unit node
    let EmptyCell = document.createElement("td");
    EmptyCell.setAttribute("style", `width: ${EmptyCellWidth}px`);
    let SelectUnit = document.createElement("select");
    SelectUnit.setAttribute("id", `unit_${amount_ingredients}`);
    SelectUnit.setAttribute("name", `unit_${amount_ingredients}`);
    let SelectGram = document.createElement("option");
    SelectGram.setAttribute("value", "g");
    SelectGram.textContent = "g";
    let SelectPiece = document.createElement("option");
    SelectPiece.setAttribute("value", "St.");
    SelectPiece.textContent = "St.";

    // create ingredient node
    let SelectIngredient = document.getElementById("ingredient_0").cloneNode("deep");
    const $default_select = SelectIngredient.querySelector("#no_ingredient");
    SelectIngredient.value = $default_select.value;
    SelectIngredient.firstElementChild.setAttribute("selected", "")
    SelectIngredient.setAttribute("id", `ingredient_${amount_ingredients}`);
    SelectIngredient.setAttribute("name", `ingredient_${amount_ingredients}`);

    // create delete button node
    let DeleteButton = document.createElement("button");
    DeleteButton.setAttribute("id", `delete_${amount_ingredients}`);
    DeleteButton.setAttribute("type", "button");
    DeleteButton.setAttribute("class", "delete_ingredient");
    DeleteButton.setAttribute("onclick", `delete_recipe_ingredient(${amount_ingredients})`);
    let DeleteIcon = document.createElement("i");
    DeleteIcon.setAttribute("class", "fa-solid fa-trash-can");

    // add row node
    NewRecipeTable.appendChild(NewRecipeIngredientTable);
    NewRecipeIngredientTable.appendChild(NewRecipeIngredientRow);

    // add cell nodes
    NewRecipeIngredientRow.appendChild(EmptyCell);
    NewRecipeIngredientRow.appendChild(InputQuantityCell);
    NewRecipeIngredientRow.appendChild(UnitCell);
    NewRecipeIngredientRow.appendChild(IngredientCell);
    NewRecipeIngredientRow.appendChild(DeleteButtonCell);

    // fill InputQuantityCell
    InputQuantityCell.appendChild(InputQuantity);

    // fill UnitCell
    SelectUnit.appendChild(SelectGram);
    SelectUnit.appendChild(SelectPiece);
    UnitCell.appendChild(SelectUnit);

    // add IngredientCell
    IngredientCell.appendChild(SelectIngredient);

    // fill DeleteButtonCell
    DeleteButton.appendChild(DeleteIcon);
    DeleteButtonCell.appendChild(DeleteButton);
}

window.onload = init;
