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
