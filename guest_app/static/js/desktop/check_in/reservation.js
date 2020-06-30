$('.reservation-container').click(function() {
    $(this).addClass('active')
        .find('input').prop('checked', true).change();
    $('.reservation-container:not(#'+ $(this).attr('id') +')').removeClass('active');
});


$('input[name=reservation]').change(function() {
    $('#btn-step-next').attr('disabled', false);
});
