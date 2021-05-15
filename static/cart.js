// Load click handler on page render 
window.onload = update_total;


// Remove item from cart
$('.trash-btn').click(function() {
    var i = $(this).data('index');
    var drink_id = $(this).data('id');

    // Remove item from session
    fetch("/remove-from-cart", {
        method: "POST",
        body: JSON.stringify({ drink_id: drink_id }),
    }).then((_res) => {
        window.location.href = "/cart";
    });

    $('#cart-item-'.concat(i)).remove();
    update_total();
})


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

    var subtotal = 0
    for (var i =0; i < cart_items.length; i++) {
        var cart_item = cart_items[i];

        var price = cart_item.getElementsByClassName('cart-price')[0].innerHTML;
        var quantity = cart_item.getElementsByClassName('cart-qty')[0].innerHTML;
        subtotal = subtotal + (price * quantity);
    }
    document.getElementById('subtotal').innerHTML = "$" + subtotal.toFixed(2).toString();

    // var tax = subtotal * 0.0775;
    // document.getElementById('tax').innerHTML = "$" + tax.toFixed(2).toString();

    // var total = tax + subtotal;
    // document.getElementById('total').innerHTML = "$" + total.toFixed(2).toString();
}


// Proceed to checkout
var checkout_button = document.getElementById('checkout');

checkout_button.addEventListener('click', function() {
    fetch('/checkout-session', {
        method: 'POST',
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(session) {
        var stripe = Stripe(session.public_key);
        return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(function(result) {
        if (result.error) {
            alert(result.error.message);
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
});
