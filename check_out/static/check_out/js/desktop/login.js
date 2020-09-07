$('#id_reservation_no, #id_last_name, #id_arrival_date').keyup(function() {
    enableDisableButton();
});
$('#id_reservation_no, #id_last_name').keyup();


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
