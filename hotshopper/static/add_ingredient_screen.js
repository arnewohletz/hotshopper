function init() {
    document.getElementById("add_ingredient_screen").style.display = "block";
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "block";
}

function cancel_close_add_ingredient() {
    document.getElementById("add_ingredient_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_ingredient_form').reset();
    window.location.href = "/ingredients"
}

function set_location(location_id) {
    document.getElementById("")
}

window.onload = init;
