
$(function() {
  $('.togglebutton').removeClass('checkbox');
  $.material.init();

  $('#id_login').blur();
  $('#id_login').focus();

  $('#login-modal').on('shown.bs.modal', function () {
    $('#id_login').focus();
  });
})
