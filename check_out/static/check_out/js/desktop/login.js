$('#id_reservation_no, #id_room_no').keyup(function() {
    enableDisableButton();
});
$('#id_reservation_no, #id_room_no').keyup();


function enableDisableButton() {
    $reservationNo = $('#id_reservation_no')
        , $roomNo = $('#id_room_no');

    if ($reservationNo.val() != '' && $roomNo.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
    }
}
