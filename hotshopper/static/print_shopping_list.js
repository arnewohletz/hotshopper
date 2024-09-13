function init() {
    document.getElementById("copyright_ruler").remove();
    document.getElementById("copyright").remove();

    let shopping_list_tables = document.getElementsByClassName("shopping_list_content");

    for (let i = 0; i < shopping_list_tables.length; i++) {
        apply_list_overflow_event_listener(shopping_list_tables[i])
        // shopping_list_tables[i].addEventListener('overflow', function() {
        //     move_overflowing_content_to_new_table(this);
        // });
    }

    let empty_amount_fields = document.getElementsByClassName("print_shopping_list_amount");
    for (let i= 0; i < empty_amount_fields.length; i++) {
        let ctx = empty_amount_fields[i].getContext('2d');
        ctx.fillStyle = "#c6c6c6ff";
        ctx.fillRect(0, 0, empty_amount_fields[i].width, empty_amount_fields[i].height);
    }
}

function move_overflowing_content_to_new_table(list_element) {
    // console.log(list_element.style["columns"]++);
    // console.log(list_element.style["columns"] + 1);
    list_element.style["columns"]++;
    list_element.style["column-fill"] = "auto";
    doubleWidthInMillimeters(list_element);
    let test_clone = list_element.cloneNode(false);
    // test_clone.innerHTML = getOverflowingTextContent(list_element);
    // let whitespace = document.createElement("a");
    // whitespace.innerHTML = "&nbsp;";
    // apply_list_overflow_event_listener(test_clone);
    // list_element.parentNode.insertBefore(test_clone, list_element.nextSibling);
    // list_element.parentNode.insertBefore(whitespace, list_element.nextSibling);
}


function apply_list_overflow_event_listener(element) {
    element.addEventListener('overflow', function () {
        move_overflowing_content_to_new_table(this);
    })
}

function doubleWidthInMillimeters(element) {
    var widthInMillimeters = parseFloat(element.style.width); // Get the current width in millimeters
    var widthInPixels = widthInMillimeters * 3.7795275591; // Convert millimeters to pixels (1 mm ≈ 3.7795275591 px)
    var doubledWidthInPixels = widthInPixels * 2; // Double the width in pixels
    var doubledWidthInMillimeters = doubledWidthInPixels / 3.7795275591; // Convert the doubled width back to millimeters
    element.style.width = doubledWidthInMillimeters + 'mm'; // Apply the doubled width in millimeters to the element
}

function back_to_main_screen() {
    window.location.href = "/show_shopping_list"
}


// function getOverflowingTextContent(element) {
//     var previousOverflow = element.style.overflow;
//     element.style.overflow = 'visible';
//
//     var overflowingText = '';
//
//     if (element.scrollHeight > element.clientHeight) {
//         var clone = element.cloneNode(true);
//         clone.style.height = 'auto';
//         clone.style.position = 'absolute';
//         clone.style.visibility = 'hidden';
//         clone.style.overflow = 'visible';
//         clone.style.maxHeight = 'none';
//         element.parentNode.appendChild(clone);
//
//         for (var i = 0; i < clone.childNodes.length; i++) {
//             var child = clone.childNodes[i];
//             if (child.offsetTop >= element.clientHeight) {
//                 overflowingText += child.textContent;
//             }
//         }
//
//         element.parentNode.removeChild(clone);
//     }
//
//     element.style.overflow = previousOverflow;
//
//     return overflowingText || null; // Return null if no overflowing text
// }


window.onload = init;

