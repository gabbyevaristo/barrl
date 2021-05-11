function myFunction(clickedID, drink) {
    let buttonID = clickedID.slice(0,-7);
    console.log(typeof(drink));
    $('#modal-title').text(drink.name);
    $("#modal-drink-image").attr("src", drink.image);
    $("#modal-drink-price").text("$" + drink.price);
    $('#quantity-modal').modal({backdrop: 'static', keyboard: false});
}

// $("button").click(function() {
//     let buttonID = $(this).attr('id');
//     let drinkData = $(this).attr('data-selector');
//     $('#modal-title').text(typeof(drinkData));
//     $('#quantityModal').modal({backdrop: 'static', keyboard: false});
// })


// drinks = $.get("/getdrinklist", function(data) {
//     console.log($.parseJSON(data))
// })
