$(document).ready(function() {
    // to auto focus
    $('input:visible').first().focus();
    
    // to enable disable button
    $('#id_last_name, #id_room_no').keyup();
});


$('#id_last_name, #id_room_no').keyup(function() {
    enableDisableButton();
});
$('#id_last_name, #id_room_no').keyup();


function enableDisableButton() {
    $reservationNo = $('#id_last_name')
        , $roomNo = $('#id_room_no');

    if ($reservationNo.val() != '' && $roomNo.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
    }
}
