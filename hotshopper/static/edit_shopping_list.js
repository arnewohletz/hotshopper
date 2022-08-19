// let draggingEle; // The dragging element
// let draggingRowIndex; // The index of dragging row
// let placeholder;
// let isDraggingStarted = false;
// let table;
// let list;
//
// // The current position of mouse relative to the dragging element
// let x = 0;
// let y = 0;

function init() {
    document.getElementById("edit_shopping_list_screen").style.display = "block";

    let tables = document.getElementsByClassName("rows_draggable")
    // table = document.getElementById("edit_locations");
    for (let i = 0; i < tables.length; i++) {
        tables[i].querySelectorAll("tr.location").forEach(function (row, index) {
            // if (index === 0) {
            //     return;
            // }

            // Add class to row
            row.classList.add("draggable");

            // Attach event handler
            row.addEventListener("mousedown", mouseDownHandler);
        });
    }

}

function close_edit_shopping_list_screen() {
    document.getElementById("edit_shopping_list_screen").style.display = "none";
    // document.getElementById("cover").style.display = "none";
    window.location.href = "/shopping_list";
}

function post_drag_action(table) {
    const location_id = table.dataset.indexNumber
    // const section_id = table.dataset.indexNumber.split("_")[1]
    let new_order = "";
    table.querySelectorAll("tr.draggable").forEach(function (row, index) {
        // if (index === 0) {
        //     return;
        // }
        new_order += `${row.dataset.indexNumber}_`
    });
    new_order = new_order.substring(0, new_order.length - 1)

    window.location.href = `/update_location_order/${new_order}`
}

window.onload = init;
