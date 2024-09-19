
function init(edit) {
    document.getElementById("recipe_screen").style.display = "grid";
    document.getElementById("cover").style.display = "grid";

    if (edit === "True") {
        document.getElementById("recipe_screen_header").innerText = "Rezept bearbeiten";
    } else {
        document.getElementById("recipe_screen_header").innerText = "Neues Rezept";
    }
}

function cancel_close_recipe_screen(edit) {
    document.getElementById("recipe_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    if (edit === "False") {
        document.getElementById('recipe_form').reset();
    }
    window.location.href = "/"
}

function confirm_close_recipe_screen() {
    let element = document.getElementById("recipe_screen");
    if (!element) {
        element = document.getElementById("recipe_form");
    }
    if (!formcheck(element)) {
        return false;
    }
    let current_scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
    let current_recipe_amount_ingredients = document.getElementsByClassName("recipe_ingredient").length;
    document.getElementById("cover").style.display = "none";
    let current_recipe_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
    const template_add = new_ingredient_index => `/confirm_new_recipe/${new_ingredient_index}_${current_scroll_height}`
    const template_edit = new_ingredient_index => `/confirm_edit_recipe/${current_recipe_id}_${new_ingredient_index}_${current_scroll_height}`

    document.getElementById("recipe_screen").style.display = "none";
    document.getElementById("recipe_form").addEventListener(
        "submit", function (s) {
            s.preventDefault();
            this.action = template_edit(current_recipe_amount_ingredients);
            this.submit();
        });
}

document.addEventListener("DOMContentLoaded", function () {
    init(edit);
});
