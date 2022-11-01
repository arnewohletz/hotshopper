let SELECTED_LOCATION_ID;

function init() {
    document.getElementById("add_ingredient_screen").style.display = "block";
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "block";
    SELECTED_LOCATION_ID = document.getElementById("selected_location_id").childNodes[0].nodeValue;

    if (SELECTED_LOCATION_ID >= 0) {
        decide_display_section(SELECTED_LOCATION_ID)
    }

    let sections = document.getElementsByClassName("section");
    for (let i = 0; i < sections.length; i++) {
        if (sections[i].id !== "section_placeholder") {
            let section = sections[i];
            sections[i].style.display = "none";
        }
    }
    document.getElementById("location_0").addEventListener("selectionchange",
        (event) => {
            document.getElementById("location_0").disabled = !event.target.id
        }, false);
}

function cancel_close_add_ingredient() {
    document.getElementById("add_ingredient_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_ingredient_form').reset();
    window.location.href = "/ingredients"
}

function decide_display_section(location_id) {
    let section_rows = document.getElementsByClassName("section");
    for (let i = 0; i < section_rows.length; i++) {
        if (section_rows[i].id === `section_${location_id}`) {
            section_rows[i].style.display = "contents";
        } else if (location_id === 0 && section_rows[i].id === "section_placeholder") {
            section_rows[i].style.display = "contents";
        } else {
            section_rows[i].style.display = "none";
        }
    }
}


function set_location() {

    let section_lists = document.getElementsByClassName("section_list");
    for (let i = 0; i < section_lists.length; i++) {
        section_lists[i].disabled = true;
    }
    document.getElementById("selected_location_id").childNodes[0].nodeValue = document.getElementById("location_0").selectedIndex;
    SELECTED_LOCATION_ID = document.getElementById("location_0").selectedIndex;


    if (SELECTED_LOCATION_ID >= 0) {
        decide_display_section(SELECTED_LOCATION_ID);
        let available_sections = document.getElementById(`location_${SELECTED_LOCATION_ID}_sections`);

        if (available_sections.length > 1) {
            available_sections.disabled = false;
        }
    }
}


window.onload = init;
