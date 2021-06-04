var alert_time = 800;
var min_quantity = 0;
var max_quantity = 4;


// Open add to cart modal
$('.item-btn').click(function() {
    var i = $(this).data('index');

    // Reset modal to prevent previous attributes and values from populating
    reset_modal(i);

    $('#modal-menu-'.concat(i)).modal({backdrop: 'static', keyboard: false});
})


// Handle increment and decrement for add to cart modal quantity selector
$('.plus-btn, .minus-btn').click(function() {
    var i = $(this).data('index');
    var sign = $(this).data('identifier');

    var quantity_string = $('#modal-menu-quantity-'.concat(i)).text();
    var quantity_int = parseInt(quantity_string);

    // Update quantity accordingly
    if (sign == "plus") {
        $('#modal-menu-quantity-'.concat(i)).text((quantity_int + 1).toString());
    } else {
        $('#modal-menu-quantity-'.concat(i)).text((quantity_int - 1).toString());
    }

    // Get updated quantity
    var updated_quantity = $('#modal-menu-quantity-'.concat(i)).text();

    // Update button disabled attribute accordingly
    if (sign == "plus") {
        $('#minus-menu-button-'.concat(i)).prop('disabled', false);
        $('#add-to-cart-button-'.concat(i)).prop('disabled', false);
        $('#modal-menu-price-'.concat(i)).prop('hidden', false);
        if (updated_quantity >= max_quantity) {
            $('#plus-menu-button-'.concat(i)).prop('disabled', true);
        }
    } else {
        $('#plus-menu-button-'.concat(i)).prop('disabled', false);
        if (updated_quantity == min_quantity) {
            $('#minus-menu-button-'.concat(i)).prop('disabled', true);
            $('#add-to-cart-button-'.concat(i)).prop('disabled', true);
            $('#modal-menu-price-'.concat(i)).prop('hidden', true);
        }
    }

    // Update price value according to quantity
    var drink_price = $('#menu-price-'.concat(i)).text();
    var price = parseInt(updated_quantity) * parseFloat(drink_price);
    $('#modal-menu-price-'.concat(i)).text("$" + price.toString());
})


// When add to cart button is clicked
$('.add-to-cart-btn').click(function() {
    var i = $(this).data('index');
    var drink_id = $(this).data('id');

    var drink_quantity = $('#modal-menu-quantity-'.concat(i)).text();
    $('#modal-menu-'.concat(i)).modal('hide');

    // Show add to cart alert for time equal to alert_time
    $('#add-to-cart-alert').show();
    setTimeout(function(){
        $('#add-to-cart-alert').hide('fade');
    }, alert_time);

    fetch("/add-to-cart", {
        method: "POST",
        body: JSON.stringify({ drink_id: drink_id, drink_quantity: drink_quantity }),
    })
    .then(response => response.json())
    .then(data => {
        // Set cart quantity
        $('#nav-cart-quantity').text(data);
    });
})


// Reset modal attributes and values
function reset_modal(i) {
    $('#modal-menu-quantity-'.concat(i)).text("0");
    $('#minus-menu-button-'.concat(i)).prop('disabled', true);
    $('#plus-menu-button-'.concat(i)).prop('disabled', false);
    $('#modal-menu-price-'.concat(i)).prop('hidden', true);
    $('#add-to-cart-button-'.concat(i)).prop('disabled', true);
}
