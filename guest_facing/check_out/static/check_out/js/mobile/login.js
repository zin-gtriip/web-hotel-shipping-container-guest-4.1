window.addEventListener("flutterInAppWebViewPlatformReady", null); // add event to send message to app
gaTag('login_last_name_display', 'check_out'); // google analytics

$(document).ready(function() {
    // to auto focus
    $('input:visible').first().focus();
    
    // to enable disable button
    $('#id_last_name, #id_room_no').keyup();
});


$('#id_last_name').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-last-name button').attr('disabled', false);
	} else {
		$('#footer-last-name button').attr('disabled', true);
	}
});


$('#id_room_no').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-room-no button').attr('disabled', false);
	} else {
		$('#footer-room-no button').attr('disabled', true);
	}
});


$('#footer-last-name button').click(function() {
	var $currentStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name')
		, $nextStep = $('#header-room-no, #subheader-room-no, #content-room-no, #footer-room-no');

	$('.header #btn-back').show();
	$('.header #btn-home').hide();
	$nextStep.show().addClass('active');
	try { window.flutter_inappwebview.callHandler('lastName', $('#id_last_name').val()); } catch(error) {} // send message to app
	gaTag('login_room_no_display', 'check_out'); // google analytics
	$currentStep.animate({opacity: 0}, {
		step: function(now) {
			// for making fielset appear animation
			opacity = 1 - now;
			$currentStep.css({'display': 'none', 'position': 'relative'});
			$nextStep.css({'opacity': opacity});
		}
		, duration: 300
	}).removeClass('active');
});



$('#footer-room-no button').click(function() {
	try { window.flutter_inappwebview.callHandler('roomNo', $('#id_room_no').val()); } catch(error) {} // send message to app
});


$('#btn-back').click(function() {
	var $currentActive = $('.content-input.active')
		, $previousStep;

	if ($currentActive.attr('id') == 'content-room-no') {
		$currentStep = $('#header-room-no, #subheader-room-no, #content-room-no, #footer-room-no');
		$previousStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name');
		$(this).hide();
		$('.header #btn-home').show();
	}

	$previousStep.show().addClass('active');
	$currentStep.animate({opacity: 0}, {
		step: function(now) {
			// for making fielset appear animation
			opacity = 1 - now;
			$currentStep.css({'display': 'none', 'position': 'relative'});
			$previousStep.css({'opacity': opacity});
		}
		, duration: 300
	}).removeClass('active');
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
