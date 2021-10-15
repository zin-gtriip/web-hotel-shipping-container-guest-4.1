// google analytics
gaTag('login_reservation_no_display', 'registration');
gaTag('login_last_name_display', 'registration');
gaTag('login_arrival_date_display', 'registration');


$(document).ready(function() {
    // to auto focus
    $('input:visible').first().focus();
    
    // to enable disable button
    $('#id_reservation_no, #id_last_name').keyup();
});

$('.datepicker').datepicker({
    startDate: new Date(),
});


if ($('#id_arrival_date').val() == '') {
    $('#id_arrival_date').datepicker('update', new Date());
}


$('#id_reservation_no, #id_last_name, #id_arrival_date').keyup(function() {
    enableDisableButton();
});


$('#id_arrival_date').datepicker().on('changeDate', function() {
    enableDisableButton();
});


$('#id_reservation_no').focusout(function() {
    if ($(this).val()) {
        gaTag('login_reservation_no_entered', 'registration');// google analytics
    }
});


$('#id_last_name').focusout(function() {
    if ($(this).val()) {
        gaTag('login_last_name_entered', 'registration');// google analytics
    }
});


$('#id_arrival_date').focusout(function() {
    if ($(this).val()) {
        gaTag('login_arrival_date_entered', 'registration');// google analytics
    }
});


function enableDisableButton() {
    $reservationNo = $('#id_reservation_no')
        , $lastName = $('#id_last_name')
        , $arrivalDate = $('#id_arrival_date');

    if ($reservationNo.val() != '' && $lastName.val() != '' && $arrivalDate.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
    }
}
