$('.datepicker').datepicker();
$('#id_arrival_date').datepicker('update', new Date());


$('input:visible').change(function() {
	var $this = $(this);
	if ($this.val() != '') {
		$('#btn-step-next').attr('disabled', false);
	} else {
		$('#btn-step-next').attr('disabled', true);
	}
});
$('input').change();


$('#btn-step-next').click(function() {
	var $currentStep = $('.input-step.active')
		, $nextStep = $currentStep.next('.input-step');

	$nextStep.find('input').change(function () {
		var $this = $(this);
		if ($this.val() != '') {
			$('#btn-step-next').attr('disabled', false);
		} else {
			$('#btn-step-next').attr('disabled', true);
		}
	});
	$('input').change();

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


$('.modal.error-modal').each(function() {
	if (!$('body').hasClass('modal-open')) {
		$(this).modal('show').addClass('shown');
	}
	// trigger next modal
	$(this).on('hidden.bs.modal', function(e) {
		$('.modal.error-modal:not(.shown)').first().modal('show').addClass('shown');
	});
});
