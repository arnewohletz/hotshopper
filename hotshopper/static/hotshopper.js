// let scroll_height;

function init() {
    // hide_shopping_list();
    window.scroll(0, scroll_height);
    // document.scroll = scroll_height;
    const calc_button = document.getElementById("calc_button");
    calc_button.addEventListener("click", shopping_list_calc);
}

function shopping_list_calc() {
    // show_shopping_list();
    const recipes_table = document.getElementById("recipe_selection")
    // for (let i = 0; i < recipes_table.rows.length; i++) {
    //     var item = recipes_table.innerText.
    // }
        console.log(recipes_table.innerHTML.id);

    var recipeSelection = JSON.stringify("#recipe_selection");
}

function set_selected(checkboxElem) {
    scroll_height = document.documentElement.scrollTop || document.body.scrollTop
    // scroll_height = document.documentElement.scrollHeight;
    if (checkboxElem.checked) {
        window.location.href = "/check_recipe/" + checkboxElem.id + "_" + scroll_height
    }
    else {
        window.location.href = "/uncheck_recipe/" + checkboxElem.id + "_" + scroll_height
    }
}


function hide_shopping_list() {
    document.getElementById("shopping_list_table").style.display = "none";
}

function show_shopping_list() {
    document.getElementById("shopping_list_table").style.display = "block";
}

window.onload = init;
