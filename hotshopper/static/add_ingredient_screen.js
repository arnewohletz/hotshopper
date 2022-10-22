function init() {
    document.getElementById("add_ingredient_screen").style.display = "block";
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "block";
    document.getElementById("location_0").addEventListener("selectionchange",
    (event) => {
        document.getElementById("location_0").disabled = !event.target.id
        // if (document.getElementById("location_0").getSelection().id === "no_location") {
        //     document.getElementById("location_0").disabled;
        // } else {
        //     document.getElementById("location_0").;
        // }
        // document.getElementById("section").disabled = !event.target.checked;
    }, false);
}

function cancel_close_add_ingredient() {
    document.getElementById("add_ingredient_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_ingredient_form').reset();
    window.location.href = "/ingredients"
}



function set_location() {
    let location = document.getElementById("location_0");
    if (location.options.selectedIndex === 0) {
        document.getElementById("section").disabled = true;

    } else {
        document.getElementById("section").disabled = false;
        console.log("Sections are available again");
    }
    window.location.href = `/add_ingredient/${location.options.selectedIndex}`


}

window.onload = init;
