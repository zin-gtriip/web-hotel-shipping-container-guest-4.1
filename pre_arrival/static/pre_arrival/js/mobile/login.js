$('.datepicker').datepicker();
$('#id_arrival_date:not(.is_bound)').datepicker('update', new Date());
try { nextPage.postMessage('/check_in/login/reservation_no'); } catch(error) {} // send message to app
var loginStep = 0;


$('#id_reservation_no, #id_last_name, #id_arrival_date').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
	}
});
$('#id_reservation_no, #id_last_name').keyup();


$('#id_arrival_date').datepicker().on('changeDate', function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
	}
});


$('#btn-step-next').click(function() {
	var $currentStep = $('.input-step.active')
		, $nextStep = $currentStep.next('.input-step');
		
	$nextStep.find('input').keyup();

	// send message to app
	loginStep += 1;
	switch(loginStep) {
		case 1:
			try { nextPage.postMessage('/check_in/login/last_name'); } catch(error) {}
			break;
		case 2:
			try { nextPage.postMessage('/check_in/login/arrival_date'); } catch(error) {}
			break;
	}

	// submit if no more nextStep
	if ($nextStep.length == 0) {
		$('#form-mobile-login').submit();
	}

	$nextStep.show().addClass('active');
	$currentStep.animate({opacity: 0}, {
		step: function(now) {
			// for making fielset appear animation
			opacity = 1 - now;
			$currentStep.css({'display': 'none', 'position': 'relative'});
			$nextStep.css({'opacity': opacity});
		}
		, duration: 1000
	}).removeClass('active');
});
