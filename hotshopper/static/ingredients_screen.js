function init() {
    document.getElementById("cover").style.display = "grid";
    document.getElementById("ingredients_screen").style.display = "grid";
    let scroll_height_ingredients = sessionStorage.getItem("scroll_height_ingredients");
    if (scroll_height_ingredients !== null) {
        scroll_height_ingredients = parseInt(scroll_height_ingredients);
    }

    if (scroll_height_ingredients > 0) {
        let table = document.getElementById("ingredients_table");
        apply_scroll_height(table, scroll_height_ingredients);
        sessionStorage.setItem("scroll_height_ingredient", "0");
    }
}

function close_ingredients_screen() {
    document.getElementById("ingredients_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    window.location.href = "/"
}

function apply_scroll_height(element, scroll_height) {
    const rule = window.getComputedStyle(element);
    const scrollable = element.scrollWidth>element.clientWidth;
    // const not_hidden = window.getComputedStyle(element).overflowY !== 'hidden';

    if (scrollable) {
        element.scroll(0, scroll_height);
    }
}

function edit_ingredient(defer_url) {
    window.location.href = `${defer_url}`;
}

function delete_ingredient(ingredient) {
    let table = document.getElementById("ingredients_table");
    sessionStorage.setItem("scroll_height_ingredients", `${table.scrollTop}`);
    // let scroll_height = table.scrollTop;
    let text = `Zutat "${ingredient.name}" wirklich löschen?`;
    let recipes = ingredient.getAttribute("data-uses-recipes");
    let recipes_array = recipes.slice(2, recipes.length - 2).split("', '");
    if (recipes_array[0].length > 0) {
        text = text + "\n\nZutat wird aktuell verwendet in:"
        for ( let i = 0; i < recipes_array.length; i++) {
            text = text + `\n${recipes_array[i]}`;
        }
        text = text + "\n\n(Zutat wird aus genannten Rezepten entfernt)";
    } else {
        text = text + "\n\n Zutat wird aktuell nicht verwendet.";
    }
    Swal.fire({
        html: '<pre>' + text + '</pre>',
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: 'Abbruch',
        confirmButtonText: 'OK',
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `${ingredient.id}`;
        }
    })
}

window.onload = init;
