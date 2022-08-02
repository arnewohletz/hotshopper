// function init() {
// document.getElementById("cover").style.display = "block";
// document.getElementById("shopping_list_screen").style.display = "block";
//
// // table = document.getElementById("shopping_list_template");
// table = document.getElementById("Kühlteigwaren");
//
// table.querySelectorAll("#Kühlteigwaren tr").forEach(function (row, index) {
//     if (index === 0) {
//         return;
//     }
//
//     // Add class to row
//     row.classList.add("draggable");
//
//     // Attach event handler
//     row.addEventListener("mousedown", mouseDownHandler);
// });
// }

function close_ingredients_screen() {
    document.getElementById("shopping_list_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    window.location.href = "/"
}

// document.addEventListener("DomContentLoaded", function () {
function init() {

    document.getElementById("cover").style.display = "block";
    document.getElementById("shopping_list_screen").style.display = "block";

    let draggingEle; // The dragging element
    let draggingRowIndex; // The index of dragging row
    var placeholder;
    let isDraggingStarted = false;
    let table;
    let list;

    // The current position of mouse relative to the dragging element
    let x = 0;
    let y = 0;

    // table = document.getElementById("shopping_list_template");
    table = document.getElementById("Kühlteigwaren");

    // Swap two nodes
    const swap = function (nodeA, nodeB) {
        const parentA = nodeA.parentNode;
        const siblingA = nodeA.nextSibling === nodeB ? nodeA : nodeA.nextSibling;

        // Move `nodeA` to before the `nodeB`
        nodeB.parentNode.insertBefore(nodeA, nodeB);

        // Move `nodeB` to before the sibling of `nodeA`
        parentA.insertBefore(nodeB, siblingA);
    };

    // Check if `nodeA` is above `nodeB`
    const isAbove = function (nodeA, nodeB) {
        // Get the bounding rectangle of nodes
        const rectA = nodeA.getBoundingClientRect();
        const rectB = nodeB.getBoundingClientRect();

        return rectA.top + rectA.height / 2 < rectB.top + rectB.height / 2;
    };

    const cloneTable = function () {
        // Get the bounding rectangle of table
        const rect = table.getBoundingClientRect();

        // Get the width of the table
        const width = parseInt(window.getComputedStyle(table).width);

        // Create new element
        list = document.createElement('div');
        list.classList.add('clone-list');

        // Set the same position as table
        // list.style.position = "absolute";
        // list.style.left = `${rect.left}px`;
        // list.style.right = `${rect.top}px`;
        list.style.position = "relative";


        // Insert it before the table
        table.parentNode.insertBefore(list, table);

        // Hide the table
        // table.style.visibility = "hidden";
        table.style.visibility = "collapse";

        table.querySelectorAll("#Kühlteigwaren tr").forEach(function (row) {
            const item = document.createElement("div");
            item.classList.add('draggable');
            const newTable = document.createElement("table");
            newTable.setAttribute('class', 'clone-table');
            newTable.style.width = `${width}px`;

            // newTable.setAttribute("class", "shopping_list_template")
            const newRow = document.createElement("tr");

            // Query the cells of row
            const cells = [].slice.call(row.children);
            cells.forEach(function (cell) {
                const newCell = cell.cloneNode(true);
                // Set the width as the original cell
                newCell.style.width = `${parseInt(window.getComputedStyle(cell).width)}px`;
                newRow.appendChild(newCell);
            });

            newTable.appendChild(newRow);
            item.appendChild(newTable);
            list.appendChild(item);
        });
    };

    const mouseDownHandler = function (e) {

        // Get the original row
        const originalRow = e.target.parentNode;
        draggingRowIndex = [].slice.call(table.querySelectorAll("tr")).indexOf(originalRow);

        // Determine the mouse position
        x = e.clientX;
        y = e.clientY;

        // Attach the listeners to `document`
        document.addEventListener('mouseup', mouseUpHandler);
        document.addEventListener('mousemove', mouseMoveHandler);

    };

    const mouseMoveHandler = function (e) {
        if (!isDraggingStarted) {
            isDraggingStarted = true;

            // if (list === undefined) {
            //     cloneTable();
            // }
            cloneTable();

            draggingEle = [].slice.call(list.children)[draggingRowIndex];
            draggingEle.classList.add('dragging');

            // Let the placeholder take the height of dragging element
            // So the next element won't move up
            placeholder = document.createElement('div');
            placeholder.classList.add('placeholder');
            draggingEle.parentNode.insertBefore(placeholder, draggingEle.nextSibling);
            placeholder.style.height = `${draggingEle.offsetHeight}px`;
        }
        // Query the dragging element
        // draggingEle = [].slice.call(list.children)[draggingRowIndex];

        // Set position for dragging element
        draggingEle.style.position = 'absolute';
        draggingEle.style.top = `${draggingEle.offsetTop + e.clientY - y}px`;
        draggingEle.style.left = `${draggingEle.offsetLeft + e.clientX - x}px`;

        // Reassign the position of mouse
        x = e.clientX;
        y = e.clientY;

        // The current order
        // prevEle
        // draggingEle
        // placeholder
        // nextEle
        const prevEle = draggingEle.previousElementSibling;
        const nextEle = placeholder.nextElementSibling;

        // The dragging element is above the previous element
        // User moves the dragging element to the top
        // We don't allow to drop above the header
        // (which doesn't have `previousElementSibling`)
        if (prevEle && prevEle.previousElementSibling && isAbove(draggingEle, prevEle)) {
            // The current order    -> The new order
            // prevEle              -> placeholder
            // draggingEle          -> draggingEle
            // placeholder          -> prevEle
            swap(placeholder, draggingEle);
            swap(placeholder, prevEle);
            return;
        }

        // The dragging element is below the next element
        // User moves the dragging element to the bottom
        if (nextEle && isAbove(nextEle, draggingEle)) {
            // The current order    -> The new order
            // draggingEle          -> nextEle
            // placeholder          -> placeholder
            // nextEle              -> draggingEle
            swap(nextEle, placeholder);
            swap(nextEle, draggingEle);
        }
    };

    const mouseUpHandler = function () {
        // Remove the placeholder
        // placeholder && placeholder.parentNode.removeChild(placeholder);

        placeholder.remove()
        // NOTE: commented out due to draggingEle is undefined error - seems OK
        // draggingEle.classList.remove('dragging');
        // draggingEle.style.removeProperty('top');
        // draggingEle.style.removeProperty('left');
        // draggingEle.style.removeProperty('position');// Remove the placeholder

        // Get the end index
        const endRowIndex = [].slice.call(list.children).indexOf(draggingEle);

        isDraggingStarted = false;

        // Remove the `list` element
        // if (list === undefined) {
        //     cloneTable();
        // }
        // else {
        //     list.parentNode.removeChild(list);
        // }
        // list.parentNode.removeChild(list);
        if (list !== undefined) {
            list.remove();
        }
        // Move the dragged row to `endRowIndex`
        let rows = [].slice.call(table.querySelectorAll("tr"));
        if (draggingRowIndex > endRowIndex) {
            // User drops to the top
            rows[endRowIndex].parentNode.insertBefore(rows[draggingRowIndex], rows[endRowIndex]);
        } else {
            // User drops to the bottom
            rows[endRowIndex].parentNode.insertBefore(rows[draggingRowIndex], rows[endRowIndex].nextSibling);
        }

        // Bring back the table
        table.style.removeProperty('visibility');

        // Remove the handlers of `mousemove` and `mouseup`
        document.removeEventListener('mouseup', mouseUpHandler);
        document.removeEventListener('mousemove', mouseMoveHandler);

        table = document.getElementById("Kühlteigwaren");

        const location_id = table.dataset.indexNumber.split("_")[0]
        const section_id = table.dataset.indexNumber.split("_")[1]
        let new_order = "";
        table.querySelectorAll("#Kühlteigwaren tr").forEach(function (row, index) {
            if (index === 0) {
            return;
        }
            new_order += `${row.dataset.indexNumber.split("_")[2]}_`
        });
        new_order = new_order.substring(0, new_order.length - 1)

        window.location.href = `/update_order/${location_id}/${section_id}/${new_order}`

    };
    table.querySelectorAll("#Kühlteigwaren tr").forEach(function (row, index) {
        if (index === 0) {
            return;
        }

        // Add class to row
        row.classList.add("draggable");

        // Attach event handler
        row.addEventListener("mousedown", mouseDownHandler);
    });
}

window.onload = init;
