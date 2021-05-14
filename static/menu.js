// Set data for modal on menu page
function open_menu_modal(drink) {
    $('#modal-drink-title').text(drink.name);
    $("#modal-drink-ingredients").text(drink.ingredients);
    $("#modal-drink-image").attr("src", drink.image);
    $("#modal-drink-price").text("$" + drink.price);
    $('#modal-menu').modal({backdrop: 'static', keyboard: false});
}

// Increment and decrement quantity for modal on menu page
$("#plus-button, #minus-button").click(function() {
    let button_id = $(this).attr('id');
    let cur_quantity_string = $("#modal-menu-quantity").text();
    let cur_quantity_int = parseInt(cur_quantity_string);

    // Update quantity accordingly
    if (button_id == "plus-button") {
        if (cur_quantity_int < 4) {
            $("#modal-menu-quantity").text((cur_quantity_int + 1).toString());
        } 
    } else {
        if (cur_quantity_int >= 1) {
            $("#modal-menu-quantity").text((cur_quantity_int - 1).toString());
        }
    }

    // Update button disabled attribute accordingly
    if (button_id == "plus-button") {
        $("#minus-button").prop('disabled', false);
        if (cur_quantity_int > 2) {
            $("#plus-button").prop('disabled', true);
        }
    } else {
        $("#plus-button").prop('disabled', false);
        if (cur_quantity_int == 1) {
            $("#minus-button").prop('disabled', true);
        }
    }
})
