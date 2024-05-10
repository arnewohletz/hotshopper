function init() {
    document.getElementById("add_recipe_screen").style.display = "block";
    document.getElementById("cover").style.display = "block";
}

function cancel_close_recipe_screen() {
    document.getElementById("add_recipe_screen").style.display = "none";
    document.getElementById("cover").style.display = "none";
    document.getElementById('add_recipe_form').reset();
    window.location.href = "/"
}

// import { add_recipe_ingredient } from "hotshopper.js"
//
// function add_recipe_ingredient(){
//     add_recipe_ingredient()
// }
//
// function confirm_close_recipe_screen(edit = false) {
//     if (!formcheck()) {
//         return;
//     }
//     let scroll_height = document.documentElement.scrollTop || document.body.scrollTop;
//     const name = document.querySelector('#recipe_name').value;
//     const ingredients = document.querySelectorAll('.recipe_ingredient');
//     // const name = new FormData(document.querySelector('#recipe_name'));
//     // const recipe = new FormData(document.querySelector('a[id="recipe_name"]'))
//     document.getElementById("ADD_RECIPE_screen").style.display = "none";
//     document.getElementById("cover").style.display = "none";
//     // let url = "/add_new_recipe/" + new_recipe_ingredients_amount;
//
//     const template_add = new_ingredient_index => `/add_new_recipe/${new_ingredient_index}_${scroll_height}`
//     const template_edit = new_ingredient_index => `/edit_recipe/${new_ingredient_index}_${scroll_height}`
//
//     if (edit) {
//         document.getElementById('EDIT_RECIPE_form').addEventListener(
//             'submit', function (s) {
//                 s.preventDefault();
//                 this.action = template_edit(new_ingredient_index);
//                 this.submit();
//             });
//     } else {
//         document.getElementById('add_recipe_form').addEventListener(
//             'submit', function (s) {
//                 s.preventDefault();
//                 this.action = template_add(new_ingredient_index);
//                 this.submit();
//             });
//     }
//
//     // window.location.href = "/add_new_recipe/" + new_recipe_ingredients_amount;
//     // window.location.href = "/add_new_recipe"
// }

window.onload = init;
