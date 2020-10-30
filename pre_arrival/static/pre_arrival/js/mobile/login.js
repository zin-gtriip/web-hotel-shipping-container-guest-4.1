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


$('#id_reservation_no').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-reservation-no button').attr('disabled', false);
	} else {
		$('#footer-reservation-no button').attr('disabled', true);
	}
});


$('#id_last_name').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-last-name button').attr('disabled', false);
	} else {
		$('#footer-last-name button').attr('disabled', true);
	}
});


$('#id_arrival_date').datepicker().on('changeDate', function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#footer-arrival-date button').attr('disabled', false);
	} else {
		$('#footer-arrival-date button').attr('disabled', true);
	}
});


$('#footer-reservation-no button').click(function() {
	var $currentStep = $('#header-reservation-no, #subheader-reservation-no, #content-reservation-no, #footer-reservation-no')
		, $nextStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name');

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


$('#footer-last-name button').click(function() {
	var $currentStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name')
		, $nextStep = $('#header-arrival-date, #subheader-arrival-date, #content-arrival-date, #footer-arrival-date');

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

	if ($currentActive.attr('id') == 'content-last-name') {
		$currentStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name');
		$previousStep = $('#header-reservation-no, #subheader-reservation-no, #content-reservation-no, #footer-reservation-no');
		$(this).hide();
	} else if ($currentActive.attr('id') == 'content-arrival-date') {
		$currentStep = $('#header-arrival-date, #subheader-arrival-date, #content-arrival-date, #footer-arrival-date');
		$previousStep = $('#header-last-name, #subheader-last-name, #content-last-name, #footer-last-name');
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
