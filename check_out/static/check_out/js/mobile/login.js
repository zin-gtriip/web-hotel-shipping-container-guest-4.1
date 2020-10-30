$('input:visible').first().focus();


$('#id_last_name').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-last-name button').attr('disabled', false);
	} else {
		$('#footer-last-name button').attr('disabled', true);
	}
});
$('#id_last_name').keyup();


$('#id_room_no').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-room-no button').attr('disabled', false);
	} else {
		$('#footer-room-no button').attr('disabled', true);
	}
});
$('#id_room_no').keyup();


$('#footer-last-name button').click(function() {
	var $currentStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name')
		, $nextStep = $('#header-room-no, #subheader-room-no, #content-room-no, #footer-room-no');

	$('.header #btn-back').show();
	$nextStep.show().addClass('active');
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


$('#btn-back').click(function() {
	var $currentActive = $('.content-input.active')
		, $previousStep;

	if ($currentActive.attr('id') == 'content-room-no') {
		$currentStep = $('#header-room-no, #subheader-room-no, #content-room-no, #footer-room-no');
		$previousStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name');
		$(this).hide();
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
