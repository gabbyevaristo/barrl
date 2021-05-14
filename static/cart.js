// Load click handler on page render (move to cart.js)
window.onload = add_click_handlers;

function delete_click_handler(event, parent) {
    event.stopPropagation();
    parent.remove();
}

function add_click_handlers() {
    var cart_list = document.getElementById("cart");
    var cart_items = cart_list.getElementsByClassName("cart-item-div");

    cart_items.forEach(function(cart_item) {
        var delete_buttons = cart_item.getElementsByClassName("btn-trash");

        delete_buttons.forEach(function(delete_button){
            delete_button.onclick = function(event) {
              return delete_click_handler(event, cart_item);
            }
        });

    });
}


// Set data for modal on cart page
function open_cart_modal(drink) {
    let cur_quantity = $("#cart-quantity").text();
    $('#modal-cart-quantity').text(cur_quantity);
    $('#modal-cart-title').text(drink.name);
    $("#modal-cart-price").text("$" + drink.price);
    $('#modal-cart').modal({backdrop: 'static', keyboard: false});
    console.log(drink);
}


// Increment and decrement quantity for modal on cart page
$("#plus-cart-button, #minus-cart-button").click(function() {
    let button_id = $(this).attr('id');
    let cur_quantity_string = $("#modal-cart-quantity").text();
    let cur_quantity_int = parseInt(cur_quantity_string);

    // Update quantity accordingly
    if (button_id == "plus-cart-button") {
        if (cur_quantity_int < 4) {
            $("#modal-cart-quantity").text((cur_quantity_int + 1).toString());
        } 
    } else {
        if (cur_quantity_int >= 2) {
            $("#modal-cart-quantity").text((cur_quantity_int - 1).toString());
        }
    }

    // Update button disabled attribute accordingly
    if (button_id == "plus-cart-button") {
        $("#minus-cart-button").prop('disabled', false);
        if (cur_quantity_int > 2) {
            $("#plus-cart-button").prop('disabled', true);
        }
    } else {
        $("#plus-cart-button").prop('disabled', false);
        if (cur_quantity_int == 2) {
            $("#minus-cart-button").prop('disabled', true);
        }
    }
})

$("#update-cart-button").click(function() {
    let cur_quantity = $("#modal-cart-quantity").text();
    $('#modal-cart').modal('hide'); 
    $('#cart-quantity').text(cur_quantity);
})
