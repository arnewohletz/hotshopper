function init() {
    document.getElementById("add_recipe_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_recipe_form').reset();
    window.scroll(0, scroll_height);
}


function set_selected(checkboxElem) {
    let scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    if (checkboxElem.checked) {
        window.location.href = "/check_recipe/" + checkboxElem.id + "_" + scroll_height;
    }
    else {
        window.location.href = "/uncheck_recipe/" + checkboxElem.id + "_" + scroll_height;
    }
}

let new_recipe_ingredients_amount = 0;

function show_add_recipe_screen() {
    new_recipe_ingredients_amount = 1;
    document.getElementById("cover").style.display = "block";
    document.getElementById("add_recipe_screen").style.display = "block";
}

function cancel_close_recipe_screen() {
    document.getElementById("add_recipe_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_recipe_form').reset();
}

function formcheck() {
    let fields = document.querySelectorAll("select,textarea, input, [required]");
    let complete = true;
    for (let field of fields) {
        if (!field.value) {
            field.style.borderColor = "red";
            complete = false;
        } else {
            field.style.borderColor = "black";
        }
    }
    return complete;
}

function confirm_close_recipe_screen() {
    if (!formcheck()) {
        return;
    }
    let scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    const name = document.querySelector('#recipe_name').value;
    const ingredients = document.querySelectorAll('.recipe_ingredient');
    // const name = new FormData(document.querySelector('#recipe_name'));
    // const recipe = new FormData(document.querySelector('a[id="recipe_name"]'))
    document.getElementById("add_recipe_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    let url = "/add_new_recipe/" + new_recipe_ingredients_amount;

    const template = new_recipe_ingredients_amount => `/add_new_recipe/${new_recipe_ingredients_amount}_${scroll_height}`
    document.getElementById('add_recipe_form').addEventListener(
        'submit', function(s) {
            s.preventDefault();
            this.action = template(new_recipe_ingredients_amount);
            this.submit();
    });
    // window.location.href = "/add_new_recipe/" + new_recipe_ingredients_amount;
    // window.location.href = "/add_new_recipe"
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
    window.location.href = "/edit_recipe/" + recipe.id;
}

function delete_recipe_ingredient(ingredient) {
    document.getElementById(ingredient);
}

function add_recipe_ingredient() {
    // increment ingredient index
    new_recipe_ingredients_amount += 1;

    // add new recipe ingredients nodes
    let NewRecipeIngredients = document.getElementById("new_recipe_ingredients");
    let NewRecipeIngredient = document.createElement("tr");
    NewRecipeIngredient.setAttribute("class", "recipe_ingredient");
    let InputQuantityCell = document.createElement("td");
    let UnitCell = document.createElement("td");
    let IngredientCell = document.createElement("td");
    let DeleteButtonCell = document.createElement("td");

    // create quantity node
    let InputQuantity = document.createElement("input");
    InputQuantity.setAttribute('size', "3");
    InputQuantity.setAttribute('id', `quantity_${new_recipe_ingredients_amount}`);
    InputQuantity.setAttribute('name', `quantity_${new_recipe_ingredients_amount}`);

    // create unit node
    let SelectUnit = document.createElement("select");
    SelectUnit.setAttribute("id",`unit_${new_recipe_ingredients_amount}`);
    SelectUnit.setAttribute("name",`unit_${new_recipe_ingredients_amount}`);
    let SelectGram = document.createElement("option");
    SelectGram.setAttribute("value", "g");
    SelectGram.textContent = "g";
    let SelectPiece = document.createElement("option");
    SelectPiece.setAttribute("value", "St.");
    SelectPiece.textContent = "St.";

    // create ingredient node
    let SelectIngredient = document.getElementById("ingredient_0").cloneNode("deep");
    SelectIngredient.setAttribute("id",`ingredient_${new_recipe_ingredients_amount}`);
    SelectIngredient.setAttribute("name",`ingredient_${new_recipe_ingredients_amount}`);

    // create delete button node
    let DeleteButton = document.createElement("button");
    DeleteButton.setAttribute("id",`delete_${new_recipe_ingredients_amount}`);
    DeleteButton.setAttribute("type","button");
    DeleteButton.setAttribute("class", "delete_ingredient");
    DeleteButton.setAttribute("onclick", "delete_recipe_ingredient(this)");
    let DeleteIcon = document.createElement("i");
    DeleteIcon.setAttribute("class", "fa-solid fa-trash-can");

    // add row node
    NewRecipeIngredients.appendChild(NewRecipeIngredient);

    // add cell nodes
    NewRecipeIngredient.appendChild(InputQuantityCell);
    NewRecipeIngredient.appendChild(UnitCell);
    NewRecipeIngredient.appendChild(IngredientCell);
    NewRecipeIngredient.appendChild(DeleteButtonCell);

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
