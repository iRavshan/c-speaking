$(document).ready(function() {
  $('#phoneNumber').inputmask("99 999-99-99", {
      removeMaskOnSubmit: true,
      clearMaskOnLostFocus: true
  });
});