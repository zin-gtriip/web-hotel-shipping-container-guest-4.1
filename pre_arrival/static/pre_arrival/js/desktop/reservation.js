var reservation = JSON.parse($('#reservation').text());

// event when reservation thumbnail is clicked
$('.reservation-container').click(function() {
    $(this).addClass('active')
        .find('input').prop('checked', true).change();
    $('.reservation-container:not(#'+ $(this).attr('id') +')').removeClass('active');
});


// enable next button when one of reservation is selected
$('input[name=reservation_no]').change(function() {
    $('#btn-step-next').attr('disabled', false);
});


// default selected value condition
if (reservation == '') {
    $('.reservation-container:first').click();
} else {
    $('input[name=reservation_no][value='+ reservation +']').parents('.reservation-container').click();
}
