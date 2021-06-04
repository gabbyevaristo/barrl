// Open last active tab
$(document).ready(function(){
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    var active_tab = localStorage.getItem('activeTab');
    if (active_tab){
        $('.nav-tabs a[href="' + active_tab + '"]').tab('show');
    }
});


// Log admin out
$('#logout').click(function() {
  fetch("/logout", {
      method: "POST"
  })
  .then(response => response.json())
  .then(data => {
      setTimeout(function(){
          window.location.reload();
      }, 100);
  });
})


// Open edit bottle modal
$('.edit-bottle-btn').click(function() {
    var id = $(this).data('id');
    $('#modal-admin-bottle-'.concat(id)).modal({backdrop: 'static', keyboard: false});
})


// Open edit drink modal
$('.edit-drink-btn').click(function() {
    var id = $(this).data('id');
    $('#modal-admin-menu-'.concat(id)).modal({backdrop: 'static', keyboard: false});
})
