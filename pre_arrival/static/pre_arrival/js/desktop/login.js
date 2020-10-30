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
