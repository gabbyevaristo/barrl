// Pour button
$('.pour-btn').click(function() {
    var i = $(this).data('index');
    var drink_id = $(this).data('id');
    
    async () => {
        await fetch("/pour-drink", {
            method: "POST",
            body: JSON.stringify({ drink_id: drink_id }),
        })
        .then((_res) => {
            window.location.href = "/pour-portal";
        })
    }

    pour_buttons = document.getElementsByClassName('pour-btn');
    pour_buttons.forEach(function(pour_button) {
        pour_button.disabled = true;
        setTimeout(function() { 
            pour_button.disabled = false;
        }, 10000);
    });

    $('#pour-item-'.concat(i)).remove();
})

