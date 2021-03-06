// google analytics
gaTag('login_reservation_no_display', 'check_out');
gaTag('login_last_name_display', 'check_out');
gaTag('login_room_no_display', 'check_out');


$(document).ready(function() {
    // to auto focus
    $('input:visible').first().focus();
    
    // to enable disable button
    $('#id_reservation_no, #id_last_name, #id_room_no').keyup();
});


$('#id_reservation_no, #id_last_name, #id_room_no').keyup(function() {
    enableDisableButton();
});
$('#id_reservation_no, #id_last_name, #id_room_no').keyup();

$('#id_reservation_no').focusout(function() {
    if ($(this).val()) {
        gaTag('login_reservation_no_entered', 'check_out');// google analytics
    }
});

$('#id_last_name').focusout(function() {
    if ($(this).val()) {
        gaTag('login_last_name_entered', 'check_out');// google analytics
    }
});


$('#id_room_no').focusout(function() {
    if ($(this).val()) {
        gaTag('login_room_no_entered', 'check_out');// google analytics
    }
});


function enableDisableButton() {
    $reservationNo = $('#id_reservation_no')
        , $lastName = $('#id_last_name')
        , $roomNo = $('#id_room_no');

    if ($reservationNo.val() != '' && $lastName.val() != '' && $roomNo.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	}else {
		$('#btn-step-next').attr('disabled', true);
    }
}
