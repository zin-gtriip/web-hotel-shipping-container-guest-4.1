$('#id_reservation_no').change(function() {
    window.location.href = window.location.origin +'/check_out/bill/'+ $(this).val();
});

$(".modal").on("hidden.bs.modal", function() {
    window.location = window.location.origin + "/check_out/complete/";
})
