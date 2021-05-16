// Pour button
// $('.pour-btn').click(function() {
//     var i = $(this).data('index');
//     var drink_id = $(this).data('id');
//     pour_buttons = document.getElementsByClassName('pour-btn');

//     var wait_for_reload = fetch("/pour-drink", {
//         method: "POST",
//         body: JSON.stringify({ drink_id: drink_id }),
//     })

//     pour_buttons.forEach(function(pour_button) {
//         pour_button.disabled = true;
//         setTimeout(function() { 
//             pour_button.disabled = false;
//         }, 10000);
//     });

//     setTimeout(function(){
//         window.location.reload();
//     }, 10000)

//     $('#pour-item-'.concat(i)).remove();
// })


window.onload = set_buttons;

function set_buttons() {
    pour_buttons = document.getElementsByClassName('pour-btn');

    pour_buttons.forEach(function(pour_button) {
        pour_button.addEventListener('click', function(e) {
            var i = $(e.target).data('index');
            var drink_id = $(e.target).data('id');
            
            fetch("/pour-drink", {
                method: "POST",
                body: JSON.stringify({ drink_id: drink_id }),
            })

            console.log(pour_buttons.length);
            if (pour_buttons.length > 1) {
                pour_buttons.forEach(function(pour_button) {
                    pour_button.disabled = true;
                    setTimeout(function() { 
                        pour_button.disabled = false;
                    }, 5000);
                });
                    
                setTimeout(function(){
                    window.location.reload();
                }, 5000);
            } else {
                setTimeout(function(){
                    window.location.reload();
                }, 1000);
            }
    
            $('#pour-item-'.concat(i)).remove();
        });
    });
}
