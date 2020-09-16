$('#id_reservation_no').change(function() {
    window.location.href = window.location.origin +'/check_out/bill/'+ $(this).val();
});
