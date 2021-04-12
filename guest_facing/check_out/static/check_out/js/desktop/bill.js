gaTag('bill_display', 'check_out'); // google analytics


if ($('.modal[id*=form-error-modal]').length >= 1) {
    gaTag('bill_checkout_fail', 'check_out'); // google analytics
}


$('#id_reservation_no').change(function() {
    window.location.href = window.location.origin +'/check_out/bill/'+ $(this).val();
});


$('.modal[id*=message-modal-]').on('hide.bs.modal', function() {
    var complete = JSON.parse($('#check-out-complete').text() || '""');
    if (complete) {
        window.location.href = '/check_out/complete/';
    }
});


$('#btn-submit').click(function() {
    gaTag('bill_checkout_button', 'check_out'); // google analytics
});
