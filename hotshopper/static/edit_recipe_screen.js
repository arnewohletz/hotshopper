function init() {
    document.getElementById("cover").style.display = "block";
    document.getElementById("edit_recipe_screen").style.display = "block";
}

function cancel_close_recipe_screen() {
    document.getElementById("edit_recipe_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    window.location.href = "/"
}


function show_recipe_screen(edit = false, recipe_id = null) {
    // let scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    //
    // let recipe_screen = document.getElementById("recipe_screen");
    // TODO: Load existing recipe
    if (edit) {
        // let name = recipe.name;
        // document.getElementById("edit_recipe_screen_title").innerHTML = "Rezept bearbeiten";
        document.getElementById("confirm_recipe").onclick = confirm_close_recipe_screen;

        document.getElementById("cover").style.display = "block";
        document.getElementById("edit_recipe_screen").style.display = "block";
    } else {
        document.getElementById("recipe_screen_title").innerHTML = "Neues Rezept";
        document.getElementById("confirm_recipe").onclick = confirm_close_recipe_screen;

        document.getElementById("cover").style.display = "block";
        document.getElementById("recipe_screen").style.display = "block";
    }

}

// function load_recipe(recipe, ingredients) {
//     for ingredient in ingredients {
//
//     }
// }

window.onload = init;
