// timer
var initialExpiryDate = JSON.parse($('#pre-arrival-initial-expiry-date').text() || '""')
    , extendedExpiryDate = JSON.parse($('#pre-arrival-extended-expiry-date').text() || '""')
    , interval = setInterval(function() { // update the count down every 1 second
        var expiryDate = extendedExpiryDate || initialExpiryDate
            , now = new Date().getTime()
            , distance
            , hours, minutes, seconds;
        expiryDate = expiryDate.slice(0, -2) + ':' + expiryDate.slice(-2, expiryDate.length); // add `:` to timezone (Safari, Firefox)
        expiryDate = new Date(expiryDate); // convert to date object
        distance = expiryDate - now; // find the distance between now and the count down date
        // time calculations for hours, minutes and seconds
        hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        seconds = Math.floor((distance % (1000 * 60)) / 1000);
        // formatting, to add 0 in front if single digit for hours, minutes, seconds
        hours = (hours.toString().length == 1) ? '0' + hours : hours;
        minutes = (minutes.toString().length == 1) ? '0' + minutes : minutes;
        seconds = (seconds.toString().length == 1) ? '0' + seconds : seconds;
        if ($('.timer-tick').length > 0) {
            // print only if have distance
            if (distance >= 0) {
                $('.timer-tick').text(minutes + ":" + seconds);
            }
            // not extended yet
            if (distance > 0 && distance <= 300000 && !extendedExpiryDate) {
                if (!$('#timer-extension-modal').hasClass('show')) {
                    $('#timer-extension-modal').modal('show');
                }
            } else if (distance <= 0) {
				$('#timer-extension-modal').modal('hide');
                clearInterval(interval);
				$('#timer-expired-modal').modal('show');
            }
        }
    }, 1000);


// timer extension
$('#form-timer-extension').submit(function() {
    event.preventDefault();
    var data = $(this).serializeArray();
    $.ajax({
        url: '/pre_arrival/timer_extension/',
        data: data,
        type: 'POST',
        success: function(result) {
            if ((result.status || 'error') == 'success') {
                if (result.pre_arrival_extended_expiry_date) {
                    extendedExpiryDate = result.pre_arrival_extended_expiry_date;
                    $('#timer-extension-modal').modal('hide');
                }
            }
        }, error: function(xhr, text, error) {
            console.error('Error client: '+ error);
        }
    });
});


// timer expired
$('#timer-expired-modal').on('hidden.bs.modal', function (e) {
    window.location.href = '/';
});


// progress bar
var currentProgressRate = JSON.parse($('#current-progress-rate').text() || '""');
$('.progress-page .progress-bar').css({
    'width': currentProgressRate +'%',
}).attr('aria-valuenow', currentProgressRate);


// header nav back button
$('.header .header-left #btn-back').click(function () {
	if ($(this).data('target') !== undefined) {
		window.location.href = $(this).data('target');
	}
});
