function init() {
    document.getElementById("cover").style.display = "block";
    document.getElementById("ingredients_screen").style.display = "block";
}

function close_ingredients_screen() {
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    window.location.href = "/"
}


window.onload = init;
