// Pour button
$('.pour-btn').click(function() {
    var i = $(this).data('index');
    var drink_id = $(this).data('id');
    
    fetch("/pour-drink", {
        method: "POST",
        body: JSON.stringify({ drink_id: drink_id }),
    })
    .then((_res) => {
        window.location.href = "/pour-portal";
    });

    $('#pour-item-'.concat(i)).remove();
})
