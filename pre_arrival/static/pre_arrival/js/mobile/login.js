window.addEventListener("flutterInAppWebViewPlatformReady", null); // add event to send message to app
try { window.flutter_inappwebview.callHandler('nextPage', '/pre_arrival/login/reservation_no'); } catch(error) {} // send message to app
var loginStep = 0;

$('.datepicker').datepicker();
if ($('#id_arrival_date').val() == '') {
	$('#id_arrival_date:not(.is_bound)').datepicker('update', new Date());
}


$('#id_reservation_no, #id_last_name, #id_arrival_date').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
	}
});
$('#id_reservation_no').keyup();


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
	$('.subheader-description').removeClass('active');

	loginStep += 1;
	switch(loginStep) {
		case 1:
			$('#subheader-last-name').addClass('active');
			try { window.flutter_inappwebview.callHandler('nextPage', '/pre_arrival/login/last_name'); } catch(error) {} // send message to app
			break;
			case 2:
				$('#subheader-arrival-date').addClass('active');
			try { window.flutter_inappwebview.callHandler('nextPage', '/pre_arrival/login/arrival_date'); } catch(error) {} // send message to app
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
