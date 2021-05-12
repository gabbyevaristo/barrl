function set_modal_data(drink) {
    $('#modal-drink-title').text(drink.name);
    $("#modal-drink-ingredients").text(drink.ingredients);
    $("#modal-drink-image").attr("src", drink.image);
    $("#modal-drink-price").text("$" + drink.price);
    $('#modal-drink').modal({backdrop: 'static', keyboard: false});
}


$("#plus-button, #minus-button").click(function() {
    let button_id = $(this).attr('id');
    let cur_quantity_string = $("#quantity-value").text();
    let cur_quantity_int = parseInt(cur_quantity_string);

    // Update quantity accordingly
    if (button_id == "plus-button") {
        if (cur_quantity_int < 4) {
            $("#quantity-value").text((cur_quantity_int + 1).toString());
        } 
    } else {
        if (cur_quantity_int >= 1) {
            $("#quantity-value").text((cur_quantity_int - 1).toString());
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
