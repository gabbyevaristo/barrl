$(document).ready(function(){
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab){
        $('.nav-tabs a[href="' + activeTab + '"]').tab('show');
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


// Set data for bottle modal
$('.edit-bottle-btn').click(function() {
    var id = $(this).data('id');
    $('#modal-admin-bottle-'.concat(id)).modal({backdrop: 'static', keyboard: false});
})


// Set data for drink modal
$('.edit-drink-btn').click(function() {
    var id = $(this).data('id');
    $('#modal-admin-menu-'.concat(id)).modal({backdrop: 'static', keyboard: false});
})
