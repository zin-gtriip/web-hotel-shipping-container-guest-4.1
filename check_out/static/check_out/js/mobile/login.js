// send message to app
try { nextPage.postMessage('/check_out/login/room_no'); } catch(error) {}


$('#id_reservation_no, #id_room_no').keyup(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
	}
});
$('#id_room_no').keyup();


$('#btn-step-next').click(function() {
	var $currentStep = $('.input-step.active')
		, $nextStep = $currentStep.next('.input-step');
		
	$nextStep.find('input').keyup();
	$('.header-description, .subheader-description').removeClass('active');

	// send message to app
	$('#header-room-no, #subheader-room-no').addClass('active');
	try { nextPage.postMessage('/check_out/login/room_no'); } catch(error) {}

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
