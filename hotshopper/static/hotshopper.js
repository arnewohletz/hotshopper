// let controller;

function init() {
    hide_shopping_list();
    const calc_button = document.getElementById("calc_button");
    calc_button.addEventListener("click", shopping_list_calc);
    console.log("Hello there!");
    console.log('{{ recipes }}');
}

function shopping_list_calc() {
    const recipes_table = document.getElementById("recipe_selection")
    // for (let i = 0; i < recipes_table.rows.length; i++) {
    //     var item = recipes_table.innerText.
    // }
        console.log(recipes_table.innerHTML.id);

    var recipeSelection = JSON.stringify("#recipe_selection");
}

function set_selected(checkboxElem) {
    if (checkboxElem.checked) {
        window.location.href = "/check_recipe/" + checkboxElem.id
    }
    else {
        window.location.href = "/uncheck_recipe/checkboxElem.name/checkboxElem.week"
    }
}


function hide_shopping_list() {
    document.getElementById("shopping_list_table").style.display = "none";
}

function show_shooping_list() {
    document.getElementById("shopping_list_table").style.display = "block";
}

window.onload = init;
