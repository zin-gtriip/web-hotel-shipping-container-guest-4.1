$('#id_reservation_no').change(function() {
    window.location.href = window.location.origin +'/check_out/bill/'+ $(this).val();
});


$('.modal[id*=message-modal-]').on('hide.bs.modal', function() {
    var complete = JSON.parse($('#check-out-complete').text() || '""');
    if (complete) {
        window.location.href = '/check_out/complete/';
    }
});
