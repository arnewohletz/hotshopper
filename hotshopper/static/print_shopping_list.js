function init() {

    // apply overflow event listener to all shopping list tables
    let shopping_list_contents = document.querySelectorAll(".shopping_list_content");
    for (let i = 0; i < shopping_list_contents.length; i++) {
        apply_list_overflow_event_listener(shopping_list_contents[i])
    }

    // add canvas field for every empty amount ingredient
    let empty_amount_fields = document.querySelectorAll(".print_shopping_list_amount");
    for (let i= 0; i < empty_amount_fields.length; i++) {
        let ctx = empty_amount_fields[i].getContext('2d');
        ctx.fillStyle = "#c6c6c6ff";
        ctx.fillRect(0, 0, empty_amount_fields[i].width, empty_amount_fields[i].height);
    }
}

function move_overflowing_content_to_new_table(list_element) {
    list_element.style["columns"]++;
    list_element.style["column-fill"] = "auto";
    doubleWidthInMillimeters(list_element);
}

function apply_list_overflow_event_listener(element) {
    element.addEventListener('overflow', function () {
        move_overflowing_content_to_new_table(this);
    })
}

function doubleWidthInMillimeters(element) {
    let widthInMillimeters = parseFloat(element.style.width); // Get the current width in millimeters
    let widthInPixels = widthInMillimeters * 3.7795275591; // Convert millimeters to pixels (1 mm ≈ 3.7795275591 px)
    let doubledWidthInPixels = widthInPixels * 2; // Double the width in pixels
    let doubledWidthInMillimeters = doubledWidthInPixels / 3.7795275591; // Convert the doubled width back to millimeters
    element.style.width = doubledWidthInMillimeters + 'mm'; // Apply the doubled width in millimeters to the element
}

function back_to_main_screen() {
    window.location.href = "/show_shopping_list"
}

window.onload = init;
