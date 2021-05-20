var wait_time = 800;

// Open modal on menu page
$('.item-btn').click(function() {
    var i = $(this).data('index');
    reset_modal(i);
    $('#modal-menu-'.concat(i)).modal({backdrop: 'static', keyboard: false});
})


// When the user clicks on add to cart
$('.add-to-cart-btn').click(function() {
    var i = $(this).data('index');
    var drink_id = $(this).data('id');
    var drink_quantity = $('#modal-menu-quantity-'.concat(i)).text();

    $('#modal-menu-'.concat(i)).modal('hide');
    reset_modal(i);

    $('#add-to-cart-alert').show();

    setTimeout(function(){
        $('#add-to-cart-alert').hide('fade');
    }, wait_time);

    fetch("/add-to-cart", {
        method: "POST",
        body: JSON.stringify({ drink_id: drink_id, drink_quantity: drink_quantity }),
    })
    .then(response => response.json())
    .then(data => {
        $('#nav-cart-quantity').text(data);
    });
})


// Reset modal attributes when modal is exited
function reset_modal(i) {
    $('#add-to-cart-button-'.concat(i)).prop('disabled', true);
    $('#modal-menu-price-'.concat(i)).prop('hidden', true);
    $('#modal-menu-quantity-'.concat(i)).text("0");
    $('#minus-menu-button-'.concat(i)).prop('disabled', true);
    $('#plus-menu-button-'.concat(i)).prop('disabled', false);
}


// Increment and decrement quantity for modal on menu page
$('.plus-btn, .minus-btn').click(function() {
    var i = $(this).data('index');  
    var sign = $(this).data('identifier'); 

    var quantity_string = $('#modal-menu-quantity-'.concat(i)).text();
    var quantity_int = parseInt(quantity_string);

    // Update quantity accordingly
    if (sign == "plus") {
        if (quantity_int < 4) {
            $('#modal-menu-quantity-'.concat(i)).text((quantity_int + 1).toString());
        } 
    } else {
        if (quantity_int >= 1) {
            $('#modal-menu-quantity-'.concat(i)).text((quantity_int - 1).toString());
        }
    }

    // Update button disabled attribute accordingly
    if (sign == "plus") {
        $('#minus-menu-button-'.concat(i)).prop('disabled', false);
        $('#add-to-cart-button-'.concat(i)).prop('disabled', false);
        $('#modal-menu-price-'.concat(i)).prop('hidden', false);
        if (quantity_int > 2) {
            $('#plus-menu-button-'.concat(i)).prop('disabled', true);
        }
    } else {
        $('#plus-menu-button-'.concat(i)).prop('disabled', false);
        // When quantity is 0 (technically)
        if (quantity_int == 1) {
            $('#minus-menu-button-'.concat(i)).prop('disabled', true);
            $('#add-to-cart-button-'.concat(i)).prop('disabled', true);
            $('#modal-menu-price-'.concat(i)).prop('hidden', true);
        }
    }

    // Get updated quantity and update price value
    var updated_quantity = $('#modal-menu-quantity-'.concat(i)).text();
    var drink_price = $('#menu-price-'.concat(i)).text();
    var price = parseInt(updated_quantity) * parseFloat(drink_price);
    $('#modal-menu-price-'.concat(i)).text("$" + price.toString());
})
