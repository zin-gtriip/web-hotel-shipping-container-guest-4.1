// timer
var expiryDate = JSON.parse($('#pre-arrival-expiry-date').text() || '""'); // set time we're counting down to
if (expiryDate) {
    expiryDate = expiryDate.slice(0, -2) + ':' + expiryDate.slice(-2, expiryDate.length); // add `:` to timezone (Safari, Firefox)
    expiryDate = new Date(expiryDate); // convert to date object
    var interval = setInterval(function() { // update the count down every 1 second
        // Get time now
        var now = new Date().getTime();
        // Find the distance between now and the count down date
        var distance = expiryDate - now;
        if (distance < 0) distance = 0;
        // Time calculations for days, hours, minutes and seconds
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        // Formatting, to add 0 in front if single digit for hours, minutes, seconds
        hours = (hours.toString().length == 1) ? '0' + hours : hours;
        minutes = (minutes.toString().length == 1) ? '0' + minutes : minutes;
        seconds = (seconds.toString().length == 1) ? '0' + seconds : seconds;
        // Output the result in an element
        $('.timer-tick').text(minutes + ":" + seconds);
        // If the count down is over
        if ($('.timer-tick').length > 0 && distance <= 0) {
            alert('Your session is expired');
            clearInterval(interval);
            window.location.href = '/';
        }
    }, 1000);
}


// progress bar
var currentPageProgressRate = JSON.parse($('#current-page-progress-rate').text() || '""');
$('.progress-page .progress-bar').css({
    'width': currentPageProgressRate +'%',
}).attr('aria-valuenow', currentPageProgressRate);


// header nav back button
$('.header .header-left #btn-back').click(function () {
	if ($(this).data('target') !== undefined) {
		window.location.href = $(this).data('target');
	}
});
