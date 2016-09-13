
$(function() {

  // this makes sure that toggle buttons are styled correctly
  $('.togglebutton').removeClass('checkbox');

  // initialize the material theme
  $.material.init();

  // not all browsers actually fire the focus event for autofocus attr
  var loginField = $('#id_login');
  loginField.focus();

  // focus on the login field when the login form is shown in a modal
  $('#login-modal').on('shown.bs.modal', function () {
    loginField.focus();
  });
})
