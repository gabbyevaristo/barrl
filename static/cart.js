// Load cart total on page render
window.onload = calculate_total;

var alert_time = 1200;
var min_quantity = 1;
var max_quantity = 20;


// Remove item from cart
$('.trash-btn').click(function() {
    var i = $(this).data('index');
    var id = $(this).data('id');

    $('#cart-item-'.concat(i)).remove();
    calculate_total();

    // Show remove from cart alert for time equal to alert_time
    $('#remove-from-cart-alert').show();
    setTimeout(function(){
        $('#remove-from-cart-alert').hide('fade');
    }, alert_time);

    fetch("/remove-from-cart", {
        method: "POST",
        body: JSON.stringify({ id: id }),
    })
    .then(response => response.json())
    .then(data => {
        // Set cart quantity
        $('#nav-cart-quantity').text(data);
        // Reload page if all items have been removed from the cart
        if (data == '') {
            setTimeout(function(){
                window.location.reload();
            }, 200);
        }
    });
})


// Open edit cart item modal
$('.edit-btn').click(function() {
    var i = $(this).data('index');

    var quantity = $('#cart-quantity-'.concat(i)).text();
    $('#modal-cart-quantity-'.concat(i)).text(quantity);

    // Set initial state of buttons when modal is first opened
    if (parseInt(quantity) == min_quantity) {
        $('#minus-cart-button-'.concat(i)).prop('disabled', true);
    } else if (parseInt(quantity) == max_quantity) {
        $('#plus-cart-button-'.concat(i)).prop('disabled', true);
    }

    // Set price value according to quantity
    var drink_price = $('#cart-price-'.concat(i)).text();
    var price = parseInt(quantity) * parseFloat(drink_price);
    $('#modal-cart-price-'.concat(i)).text("$" + price.toString());

    $('#modal-cart-'.concat(i)).modal({backdrop: 'static', keyboard: false});
})


// Handle increment and decrement for edit cart item modal quantity selector
$('.plus-btn, .minus-btn').click(function() {
    var i = $(this).data('index');
    var sign = $(this).data('identifier');

    var quantity_string = $('#modal-cart-quantity-'.concat(i)).text();
    var quantity_int = parseInt(quantity_string);

    // Update quantity accordingly
    if (sign == "plus") {
        $('#modal-cart-quantity-'.concat(i)).text((quantity_int + 1).toString());
    } else {
        $('#modal-cart-quantity-'.concat(i)).text((quantity_int - 1).toString());
    }

    // Get updated quantity
    var updated_quantity = $('#modal-cart-quantity-'.concat(i)).text();

    // Update button disabled attribute accordingly
    if (sign == "plus") {
        $('#minus-cart-button-'.concat(i)).prop('disabled', false);
        if (updated_quantity >= max_quantity) {
            $('#plus-cart-button-'.concat(i)).prop('disabled', true);
        }
    } else {
        $('#plus-cart-button-'.concat(i)).prop('disabled', false);
        if (updated_quantity == min_quantity) {
            $('#minus-cart-button-'.concat(i)).prop('disabled', true);
        }
    }

    // Update price value according to quantity
    var drink_price = $('#cart-price-'.concat(i)).text();
    var price = parseInt(updated_quantity) * parseFloat(drink_price);
    $('#modal-cart-price-'.concat(i)).text("$" + price.toFixed(2).toString());
})


// When update cart button is clicked
$('.update-btn').click(function() {
    var i = $(this).data('index');
    var id = $(this).data('id');

    var updated_quantity = $('#modal-cart-quantity-'.concat(i)).text();
    $('#cart-quantity-'.concat(i)).text(updated_quantity);
    calculate_total();
    $('#modal-cart-'.concat(i)).modal('hide');

    // Show edit cart item alert for time equal to alert_time
    $('#edited-from-cart-alert').show();
    setTimeout(function(){
        $('#edited-from-cart-alert').hide('fade');
    }, alert_time);

    fetch("/edit-cart", {
        method: "POST",
        body: JSON.stringify({ id: id, updated_quantity: updated_quantity }),
    })
    .then(response => response.json())
    .then(data => {
        // Set cart quantity
        $('#nav-cart-quantity').text(data);
    });
})


// Reset modal attributes and values if modal was closed out
$('.reset-modal').click(function() {
    var i = $(this).data('index');
    var quantity = $('#cart-quantity-'.concat(i)).text();
    if (parseInt(quantity) == min_quantity) {
        $('#minus-cart-button-'.concat(i)).prop('disabled', true);
        $('#plus-cart-button-'.concat(i)).prop('disabled', false);
    } else if (parseInt(quantity) == max_quantity) {
        $('#minus-cart-button-'.concat(i)).prop('disabled', false);
        $('#plus-cart-button-'.concat(i)).prop('disabled', true);
    } else {
        $('#minus-cart-button-'.concat(i)).prop('disabled', false);
        $('#plus-cart-button-'.concat(i)).prop('disabled', false);
    }
})


// Calculate total
function calculate_total() {
    var cart_items = document.getElementsByClassName('cart-item');
    var subtotal = 0
    for (var i = 0; i < cart_items.length; i++) {
        var price = cart_items[i].getElementsByClassName('cart-price')[0].innerText;
        var quantity = cart_items[i].getElementsByClassName('cart-qty')[0].innerText;
        subtotal = subtotal + (price * quantity);
    }
    document.getElementById('subtotal').innerText = "$" + subtotal.toFixed(2).toString();
}


// When proceed to checkout is clicked
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
