function init() {
    window.scroll(0, scroll_height);
}


function set_selected(checkboxElem) {
    let scroll_height = document.documentElement.scrollTop || document.body.scrollTop
    if (checkboxElem.checked) {
        window.location.href = "/check_recipe/" + checkboxElem.id + "_" + scroll_height
    }
    else {
        window.location.href = "/uncheck_recipe/" + checkboxElem.id + "_" + scroll_height
    }
}


window.onload = init;
