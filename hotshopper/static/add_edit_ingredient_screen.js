function init(edit) {
    document.getElementById("ingredient_screen").style.display = "block";
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "block";

    if (edit === "True") {
        document.getElementById("ingredient_screen_headline").innerText="Zutat bearbeiten";
        document.getElementById("ingredient_name").innerText=`${ingredient.name}`;
    } else {
        document.getElementById("ingredient_screen_headline").innerText="Neue Zutat";
    }

    decide_display_section(selected_location_id)
    set_location()

    document.getElementById("location").addEventListener("selectionchange",
        (event) => {
            document.getElementById("location").disabled = !event.target.id
        }, false);
}

function cancel_close_ingredient() {
    document.getElementById('ingredient_form').reset();
    window.location.href = "/ingredients";
}

function confirm_ingredient(edit) {
    if (!formcheck()) {
        return false;
    }

    let location_selection = document.getElementById("location")
    const location_index = location_selection.options[location_selection.selectedIndex].getAttribute("location_id");
    let section_index = document.getElementById(`location_${location_index}_section_selection`).selectedIndex;
    if (section_index === 0) {
        section_index = -1;
    }

    let elem_non_food = document.getElementById("non_food");
    let non_food = !!elem_non_food.checked;

    let url;
    if (edit === "True") {
        let ingredient_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);
        url = `/confirm_edit_ingredient/${ingredient_id}`
    } else {
        url = "/confirm_add_ingredient"
    }
    const template = (location_index) => `${url}/${location_index}_${section_index}_${non_food}`;

    const form = document.getElementById("ingredient_form");
    const form_data = new Map(new FormData(form).entries());

    form.addEventListener(
    "submit", async function (s) {
        s.preventDefault();
        const response = await fetch(template(location_index), {
            method: "POST",
            header: {"Content-Type": "application/json"},
            body: JSON.stringify(Object.fromEntries(form_data))
        })
        if (response.status === 409) {
            Swal.fire({
                text: `Eine Zutat namens "${form_data.get("ingredient_name")}" ist bereits vorhanden.
                Bitte einen anderen Namen wählen.`,
                icon: 'warning',
                showCancelButton: false,
                confirmButtonText: 'OK',
            }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById("ingredient_name").style.borderColor = "red";
                }
            })
        } else {
            document.getElementById("ingredient_screen").style.display = "none";
            window.location.href = "/ingredients";
        }
    }, { once: true });
}

function formcheck() {
    let fields = $("select").filter(":visible")
    let complete = true;
    for (let field of fields) {
        let has_children = field.childElementCount > 0
        let is_enabled = !field.disabled
        if (has_children && is_enabled) {
            if (field.selectedIndex === 0) {
                field.style.borderColor = "red";
                complete = false;
            } else {
                field.style.borderColor = "black";
            }
        }
    }
    return complete;
}

function decide_display_section(location_id) {
    let section_rows = document.getElementsByClassName("section");
    for (let i = 0; i < section_rows.length; i++) {
        if (section_rows[i].id === `location_${location_id}_sections`) {
            section_rows[i].style.display = "contents";
        } else if (location_id === "-1" && section_rows[i].id === "section_placeholder") {
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
    let location_select = document.querySelector("#location");
    selected_location_id = location_select.options[location_select.selectedIndex].getAttribute('location_id');

    if (selected_location_id >= 0) {
        decide_display_section(selected_location_id);
        let available_sections = document.getElementById(`location_${selected_location_id}_section_selection`);

        if (available_sections.length > 1) {
            available_sections.disabled = false;
        }
    }
}

window.onload = function() {
    init(edit);
}
