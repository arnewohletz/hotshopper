function init() {
    window.scroll(0, scroll_height);
}

// function shopping_list_calc() {
//     const recipes_table = document.getElementById("recipe_selection")
//     // for (let i = 0; i < recipes_table.rows.length; i++) {
//     //     var item = recipes_table.innerText.
//     // }
//         console.log(recipes_table.innerHTML.id);
//
//     var recipeSelection = JSON.stringify("#recipe_selection");
// }

function set_selected(checkboxElem) {
    let scroll_height = document.documentElement.scrollTop || document.body.scrollTop
    if (checkboxElem.checked) {
        window.location.href = "/check_recipe/" + checkboxElem.id + "_" + scroll_height
    }
    else {
        window.location.href = "/uncheck_recipe/" + checkboxElem.id + "_" + scroll_height
    }
}

// function hide_shopping_list() {
//     document.getElementById("shopping_list_table").style.display = "none";
// }
//
// function show_shopping_list() {
//     document.getElementById("shopping_list_table").style.display = "block";
// }

window.onload = init;
