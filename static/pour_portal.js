window.onload = set_buttons;

var wait_time = 50000;

function set_buttons() {
    pour_buttons = document.getElementsByClassName('pour-btn');

    pour_buttons.forEach(function(pour_button) {
        pour_button.addEventListener('click', function(e) {
            var i = $(e.target).data('index');
            var drink_id = $(e.target).data('id');

            pour_buttons.forEach(function(pour_button) {
                pour_button.disabled = true;
                setTimeout(function() { 
                    pour_button.disabled = false;
                }, wait_time);
            });

            var drink_name = $('#drink-name-'.concat(i)).text();
            $('#poured-drink').text('Pouring ' + drink_name);

            $(".progress-bar").animate({
                width: "100%"
            }, wait_time, function() {
                $('.progress-bar').css("width","0%");
                $('#poured-drink').text('');
            });

            fetch("/pour-drink", {
                method: "POST",
                body: JSON.stringify({ drink_id: drink_id }),
            })
            .then(response => response.json())
            .then(data => {
                // Reload page if all items have been poured
                if (data == '') {
                    setTimeout(function(){
                        window.location.reload();
                    }, wait_time);
                }
            });
    
            $('#pour-item-'.concat(i)).remove();
        });
    });
}
