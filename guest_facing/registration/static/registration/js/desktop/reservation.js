var reservationNo = JSON.parse($('#reservation').text() || '""');
gaTag('reservation_list_room', 'registration'); // google analytics


// event when reservation thumbnail is clicked
$('.reservation-container').click(function() {
    $(this).addClass('active')
        .find('input').prop('checked', true).change();
    $('.reservation-container:not(#'+ $(this).attr('id') +')').removeClass('active');
    gaTag('reservation_room_selected', 'registration'); // google analytics
});


// enable next button when one of reservation is selected
$('input[name=reservation_no]').change(function() {
    $('#btn-step-next').attr('disabled', false);
});


// default selected value condition
if (reservationNo == '') {
    $('.reservation-container:first').click();
} else {
    $('input[name=reservation_no][value='+ reservationNo +']').parents('.reservation-container').click();
}
