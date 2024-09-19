let EVEN_ROW_BACKGROUND;
let ODD_ROW_BACKGROUND;

function init() {
    // reset recipe filter input field
    document.getElementById("recipesFilter").value = "";

    // define recipe row background color
    let even_row_elem = document.getElementsByClassName("recipe_selection_AAA").item(1)
    let odd_row_elem = document.getElementsByClassName("recipe_selection").item(0)
    if (even_row_elem === null) {
        // fallback if less than two recipes are defined
        even_row_elem = odd_row_elem = document.getElementById("food_plan")
    }
    EVEN_ROW_BACKGROUND = getComputedStyle(even_row_elem).getPropertyValue("background")
    ODD_ROW_BACKGROUND = getComputedStyle(odd_row_elem).getPropertyValue("background")

    // maintain scroll height
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
    window.location.href = "/add_recipe"
}

function show_add_ingredient_screen() {
    window.location.href = "/ingredients/new"
}

function show_ingredients_screen() {
    window.location.href = "/ingredients"
}

function show_shopping_list_screen() {
    window.location.href = "/shopping_list/0"
}

function filter_recipes() {
    let total_filtered = 0;
    let filter_input = document.getElementById("recipesFilter");
    let filter = filter_input.value.toUpperCase();
    let recipe_table = document.getElementById("recipesTableBody");
    let recipe_rows = recipe_table.getElementsByClassName("recipe_selection");

    for (let i = 0; i < recipe_rows.length; i++) {
        let name_elem = recipe_rows[i].getElementsByClassName("recipe_name")[0];
        if (name_elem) {
            let name = name_elem.innerText || name_elem.textContent;
            if (name.toUpperCase().indexOf(filter) > -1) {
                recipe_rows[i].style.display = "";
                total_filtered++;
                if (total_filtered % 2 === 0) {
                    recipe_rows[i].style.background = EVEN_ROW_BACKGROUND;
                } else {
                    recipe_rows[i].style.background = ODD_ROW_BACKGROUND;
                }
                recipe_rows[i].classList.add('filtered');
            } else {
                recipe_rows[i].style.display = "none";
            }
        }
    }
}

function reset_recipe_selection() {
    window.location.href ="/reset_recipe_selection"
}

function formcheck(element) {
    let fields = element.querySelectorAll("select, textarea, input, [required]")
    let complete = true;
    for (let field of fields) {
        if (!recipe_field_contains_valid_value(field)) {
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

function recipe_field_contains_valid_value(field) {
    const ingredient_regex = /ingredient_\d+/
    if (ingredient_regex.test(field.id)) {
        return field.options[field.selectedIndex].id !== "no_ingredient";
    } else {
        return field.value !== "";
    }
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

function delete_recipe_ingredient(index) {
    let recipe_ingredients = document.getElementById("recipe_ingredients").getElementsByClassName("recipe_ingredient");
    amount_ingredients = recipe_ingredients.length;
    document.getElementById(`recipe_ingredient_${index}`).remove();

    // loop through all recipe_ingredient elements from deleted ingredient_id until end
    // and decrease index by 2 (as 'add' button is part of the recipe_ingredients div)
    for (var i = index; i < amount_ingredients - 2; i++) {
        // update recipe_ingredient element id
        let ri = recipe_ingredients[i];
        ri.id = `recipe_ingredient_${i}`;
        // update all other ids
        let quantity_element = document.querySelector(`#recipe_ingredient_${i} #quantity_${i + 1}`);
        quantity_element.id = `quantity_${i}`;
        quantity_element.name = `quantity_${i}`;
        let unit_element = document.querySelector(`#recipe_ingredient_${i} #unit_${i + 1}`);
        unit_element.id = `unit_${i}`;
        unit_element.name = `unit_${i}`;
        let ingredient_elem = document.querySelector(`#recipe_ingredient_${i} #ingredient_${i + 1}`);
        ingredient_elem.id = `ingredient_${i}`;
        ingredient_elem.name = `ingredient_${i}`;
        let delete_button = document.querySelector(`#recipe_ingredient_${i} #delete_${i + 1}`);
        delete_button.id = `delete_${i}`;
        delete_button.onclick = function() {
            delete_recipe_ingredient(i);
        };
    }
}

function add_recipe_ingredient() {

    // get new ingredient index
    let recipe_ingredients = document.getElementById("recipe_ingredients").getElementsByClassName("recipe_ingredient");
    let last_recipe_ingredient = recipe_ingredients[recipe_ingredients.length - 1];
    let parts = last_recipe_ingredient.id.split('_');
    let new_recipe_ingredient_index = (parseInt(parts[parts.length - 1]) + 1).toString();

    // add new recipe ingredients nodes
    let NewRecipeIngredientsGrid = document.getElementById("recipe_ingredients");
    let NewRecipeIngredientRow = document.createElement("div");
    NewRecipeIngredientRow.setAttribute("class", "recipe_ingredient");
    NewRecipeIngredientRow.setAttribute("id", `recipe_ingredient_${new_recipe_ingredient_index}`);
    let QuantityDiv = document.createElement("div");
    let UnitDiv = document.createElement("div");
    let IngredientNameDiv = document.createElement("div")
    let DeleteButtonDiv = document.createElement("div")

    // create quantity node
    let Quantity = document.createElement("input");
    Quantity.setAttribute('type', "number");
    Quantity.setAttribute('size', "3");
    Quantity.setAttribute('id', `quantity_${new_recipe_ingredient_index}`);
    Quantity.setAttribute('name', `quantity_${new_recipe_ingredient_index}`);
    Quantity.setAttribute('class', 'quantity');
    Quantity.setAttribute('min', '0.0');
    Quantity.setAttribute('max', '10000.0');
    Quantity.setAttribute('required', "");

    // create unit node
    let SelectUnit = document.createElement("select");
    SelectUnit.setAttribute("id", `unit_${new_recipe_ingredient_index}`);
    SelectUnit.setAttribute("name", `unit_${new_recipe_ingredient_index}`);
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
    SelectIngredient.setAttribute("id", `ingredient_${new_recipe_ingredient_index}`);
    SelectIngredient.setAttribute("name", `ingredient_${new_recipe_ingredient_index}`);

    // create delete button node
    let DeleteButton = document.createElement("button");
    DeleteButton.setAttribute("id", `delete_${new_recipe_ingredient_index}`);
    DeleteButton.setAttribute("type", "button");
    DeleteButton.setAttribute("class", "delete_ingredient");
    DeleteButton.setAttribute("onclick", `delete_recipe_ingredient(${new_recipe_ingredient_index})`);
    let DeleteIcon = document.createElement("i");
    DeleteIcon.setAttribute("class", "fa-solid fa-trash-can");

    // add row node
    let AddRecipeIngredientButtonRow = document.getElementById("recipe_ingredient_add_button");
    NewRecipeIngredientsGrid.insertBefore(NewRecipeIngredientRow, AddRecipeIngredientButtonRow)

    // add cell nodes
    NewRecipeIngredientRow.appendChild(QuantityDiv);
    NewRecipeIngredientRow.appendChild(UnitDiv);
    NewRecipeIngredientRow.appendChild(IngredientNameDiv);
    NewRecipeIngredientRow.appendChild(DeleteButtonDiv);

    // fill QuantityDiv
    QuantityDiv.appendChild(Quantity);

    // fill UnitDiv
    SelectUnit.appendChild(SelectGram);
    SelectUnit.appendChild(SelectPiece);
    UnitDiv.appendChild(SelectUnit);

    // add IngredientName
    IngredientNameDiv.appendChild(SelectIngredient);

    // add DeleteButtonDiv
    DeleteButton.appendChild(DeleteIcon);
    DeleteButtonDiv.appendChild(DeleteButton);
}

document.addEventListener("DOMContentLoaded", function () {
    let recipesFilterResetButton = document.getElementById("recipesFilterResetButton");
    recipesFilterResetButton.addEventListener("click", function() {
        document.getElementById('recipesFilter').value = '';
        filter_recipes()
    });
});

window.onload = init;
