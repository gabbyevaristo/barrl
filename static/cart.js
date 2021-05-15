// Load click handler on page render 
window.onload = function() {
    var cart_items = document.getElementsByClassName('cart-item');

    cart_items.forEach(function(cart_item) {
        var delete_buttons = cart_item.getElementsByClassName('trash-btn');

        delete_buttons[0].onclick = function(event) {
            return delete_click_handler(event, cart_item);
        }
    });

    update_total();
}


function delete_click_handler(event, parent) {
    event.stopPropagation();
    parent.remove();
    update_total();
}


// Set data for modal on cart page
$('.edit-btn').click(function() {
    var i = $(this).data('index');

    var quantity = $('#cart-quantity-'.concat(i)).text();
    $('#modal-cart-quantity-'.concat(i)).text(quantity);

    // Multiply drink price and quantity
    var price = $('#cart-price-'.concat(i)).text();
    var total_price = parseInt(quantity) * parseFloat(price);
    $('#modal-cart-price-'.concat(i)).text("$" + total_price.toString());

    // Set initial state of buttons when modal is first opened
    if (parseInt(quantity) == 1) {
        $('#minus-cart-button-'.concat(i)).prop('disabled', true);
    } else if (parseInt(quantity) == 4) {
        $('#plus-cart-button-'.concat(i)).prop('disabled', true);
    }
    
    $('#modal-cart-'.concat(i)).modal({backdrop: 'static', keyboard: false});
})


// Increment and decrement quantity for modal on cart page
$('.plus-btn, .minus-btn').click(function() {
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
    var drink_id = $(this).data('id');
    var updated_quantity = $('#modal-cart-quantity-'.concat(i)).text();
    $('#cart-quantity-'.concat(i)).text(updated_quantity);
    $('#modal-cart-'.concat(i)).modal('hide'); 

    // Edit quantity in session
    fetch("/edit-cart", {
        method: "POST",
        body: JSON.stringify({ drink_id: drink_id, updated_quantity: updated_quantity }),
    }).then((_res) => {
        window.location.href = "/cart";
    });

    update_total();
})


// Reset button state if modal was closed out
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


function update_total() {
    var cart_items = document.getElementsByClassName('cart-item');

    var total = 0
    for (var i =0; i < cart_items.length; i++) {
        var cart_item = cart_items[i];

        var price = cart_item.getElementsByClassName('cart-price')[0].innerHTML;
        var quantity = cart_item.getElementsByClassName('cart-qty')[0].innerHTML;
        total = total + (price * quantity);
    }
    total = Math.round(total * 100) / 100
    document.getElementById('subtotal').innerHTML = "$" + total.toString();
}
