// Load click handler on page render 
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

        delete_buttons[0].onclick = function(event) {
            return delete_click_handler(event, cart_item);
        }
    });
}


// Set data for modal on cart page
function open_cart_modal(drink, i) {
    var quantity = $("#cart-quantity-".concat(i)).text();
    $('#modal-cart-quantity-'.concat(i)).text(quantity);
    $('#modal-cart-title-'.concat(i)).text(drink.name);
    
    // Multiply drink price and quantity
    var price = parseInt(quantity) * parseFloat(drink.price);
    $('#modal-cart-price-'.concat(i)).text("$" + price.toString());
    $('#modal-cart-'.concat(i)).modal({backdrop: 'static', keyboard: false});
}


// Increment and decrement quantity for modal on cart page
$(".plus-btn, .minus-btn").click(function() {
    var i = $(this).data('index');          
    var sign = $(this).data('identifier');

    var quantity_string = $('#modal-cart-quantity-'.concat(i)).text();
    var quantity_int = parseInt(quantity_string);

    // Update quantity accordingly
    if (sign == "plus") {
        if (quantity_int < 4) {
            $('#modal-cart-quantity-'.concat(i)).text((quantity_int + 1).toString());
        } 
    } else {
        if (quantity_int >= 2) {
            $('#modal-cart-quantity-'.concat(i)).text((quantity_int - 1).toString());
        }
    }

    // Update button disabled attribute accordingly
    if (sign == "plus") {
        $('#minus-cart-button-'.concat(i)).prop('disabled', false);
        if (quantity_int > 2) {
            $('#plus-cart-button-'.concat(i)).prop('disabled', true);
        }
    } else {
        $('#plus-cart-button-'.concat(i)).prop('disabled', false);
        if (quantity_int == 2) {
            $('#minus-cart-button-'.concat(i)).prop('disabled', true);
        }
    }



    // Get updated quantity and update price value
    var updated_quantity = $('#modal-cart-quantity-'.concat(i)).text();
    var drink_price = $('#cart-price-'.concat(i)).text();
    var price = parseInt(updated_quantity) * parseFloat(drink_price);
    $('#modal-cart-price-'.concat(i)).text("$" + price.toString());
})

// Update cart with edited quantity values
$('.update-btn').click(function() {
    var i = $(this).data('index');
    var quantity = $('#modal-cart-quantity-'.concat(i)).text();
    $('#modal-cart-'.concat(i)).modal('hide'); 
    $('#cart-quantity-'.concat(i)).text(quantity);
})


// Reset buttons if modal was closed out (changes should not be saved)
$('.reset-modal').click(function() {
    var i = $(this).data('index');
    var quantity = $('#cart-quantity-'.concat(i)).text();
    if (parseInt(quantity) == 1) {
        $('#minus-cart-button-'.concat(i)).prop('disabled', true);
        $('#plus-cart-button-'.concat(i)).prop('disabled', false);
    } else if (parseInt(quantity) == 4) {
        $('#minus-cart-button-'.concat(i)).prop('disabled', false);
        $('#plus-cart-button-'.concat(i)).prop('disabled', true);
    } else {
        $('#minus-cart-button-'.concat(i)).prop('disabled', false);
        $('#plus-cart-button-'.concat(i)).prop('disabled', false);
    }
})