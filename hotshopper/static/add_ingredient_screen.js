let SELECTED_LOCATION_ID;
let SELECTED_SECTION_ID;
let submit_request = new XMLHttpRequest();

// function init(edit=false) {
function init() {
    document.getElementById("ingredient_screen").style.display = "block";
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "block";
    SELECTED_LOCATION_ID = document.getElementById("selected_location_id").childNodes[0].nodeValue;

    if (SELECTED_LOCATION_ID >= 0) {
        decide_display_section(SELECTED_LOCATION_ID)
    }

    let sections = document.getElementsByClassName("section");
    for (let i = 0; i < sections.length; i++) {
        if (sections[i].id !== "section_placeholder") {
            sections[i].style.display = "none";
        }
    }
    document.getElementById("location").addEventListener("selectionchange",
        (event) => {
            document.getElementById("location").disabled = !event.target.id
        }, false);

    // Register DuplicateIngredientErrorHandlerListener
    window.addEventListener(XMLHttpRequest, submit_request);
}

function cancel_close_add_ingredient() {
    document.getElementById("add_ingredient_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_ingredient_form').reset();
    window.location.href = "/ingredients"
}

function confirm_add_ingredient(edit = false) {
    if (!formcheck()) {
        return false;
    }
    // const name = document.getElementById("ingredient_name").value;
    const location_index = document.getElementById("location").selectedIndex;
    let section_index = document.getElementById(`location_${location_index}_sections`).selectedIndex;
    if (section_index === 0) {
        section_index = -1;
    }

    let elem_always_on_list = document.getElementById("always_on_shopping_list");
    let always_on_list;
    let non_food;
    // always_on_list = elem_always_on_list.selectedIndex === 1;
    let elem_non_food = document.getElementById("non_food");
    non_food = !!elem_non_food.checked;

    const template_add = (location_index) => `/confirm_new_ingredient/${location_index}_${section_index}_${non_food}`;
    const template_edit = (location_index) => `/confirm_edit_ingredient/${location_index}_${section_index}_${non_food}`;

    let form = document.getElementById("ingredient_form");
    const form_data = new Map(new FormData(form).entries());

    try {
        if (edit) {
            document.getElementById("ingredient_screen").display = "none";
            form.addEventListener(
                "submit", async function (s) {
                    s.preventDefault();
                    const response = await fetch(template_edit(location_index), {
                        method: "POST",
                        header: {"Content-Type": "application/json"},
                        body: JSON.stringify(Object.fromEntries(form_data))
                    });
                    const result = await response.json();
                    console.log(result);
                    // this.action = template_edit(location_index);
                    // submit_request.open("POST", template_edit(location_index),
                    //     {"Content-Type": "application/json"},
                    //     JSON.stringify(Object.fromEntries(form_data)));
                    // submit_request.send(this);
                    // this.submit();
                }
            );
        } else {

            form.addEventListener(
                "submit", async function (s) {
                    s.preventDefault();
                    const response = await fetch(template_add(location_index), {
                        method: "POST",
                        header: {"Content-Type": "application/json"},
                        body: JSON.stringify(Object.fromEntries(form_data))
                    })
                    const result = await response.json();
                    if (result === "400") {
                        // TODO: Add pop-up "Duplicate Ingredient"
                    } else {
                        document.getElementById("ingredient_screen").style.display = "none";
                    }

                    console.log(result);
                    // this.action = template_add(location_index);
                    // submit_request.open("POST", template_add(location_index));
                    // submit_request.send(this);
                    // this.submit();
                }
            );
        }

        if (submit_request.status === 507) {
            alert(`Duplicate ingredient: ${this.name}`);
        }
    } catch (err) {
        Swal.fire({
            text: `Zutat ${form_data["ingredient_name"]} bereits vorhanden. Bitte wählen einen anderen Namen`,
            icon: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Abbruch',
            confirmButtonText: 'OK',
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = recipe.id + "_" + scroll_height;
            }
        })
    }
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
    let location_select = document.querySelector("#location");
    SELECTED_LOCATION_ID = location_select.options[location_select.selectedIndex].getAttribute('location_id');
// TODO: False location_id is saved -> probably again the SelectedIndex instead of real id

    if (SELECTED_LOCATION_ID >= 0) {
        decide_display_section(SELECTED_LOCATION_ID);
        let available_sections = document.getElementById(`location_${SELECTED_LOCATION_ID}_sections`);

        if (available_sections.length > 1) {
            available_sections.disabled = false;
        }
    }
}

// const urlParams = new URLSearchParams(window.location.search);
// const edit = urlParams.get("edit") === "true";
// window.onload = function () {
//     init(edit);
// }
window.onload = init;
