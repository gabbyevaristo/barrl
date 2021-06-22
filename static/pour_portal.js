var pour_time = 3000;


$('.pour-btn').click(function() {
    // When pour button is clicked
    var i = $(this).data('index');
    var id = $(this).data('id');

    // Disable all other pour buttons for time equal to pour_time
    pour_buttons = document.getElementsByClassName('pour-btn');
    pour_buttons.forEach(function(pour_button) {
        pour_button.disabled = true;
        setTimeout(function() {
            pour_button.disabled = false;
        }, pour_time);
    });

    // Get currently poured drink name and set it as the value in
    // the progress bar
    var drink_name = $('#drink-name-'.concat(i)).text();
    $('#poured-drink').text('Pouring ' + drink_name);

    $('#pour-item-'.concat(i)).remove();

    // Show progress bar animation for time equal to pour_time
    $(".progress-bar").animate({
        width: "100%"
    }, pour_time, function() {
        $('.progress-bar').css("width","0%");
        $('#poured-drink').text('');
    });

    fetch("/pour-drink", {
        method: "POST",
        body: JSON.stringify({ id: id }),
    })
    .then(response => response.json())
    .then(data => {
    // Reload page if all items have been poured
        if (data == '') {
            setTimeout(function(){
                window.location.reload();
            }, pour_time);
        }
    });
})
