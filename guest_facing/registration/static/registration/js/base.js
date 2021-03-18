// timer
var expiryDuration = JSON.parse($('#session-initial-expiry-duration').text() || '""')
    , expiryDate
    , interval;
if (expiryDuration) {
    expiryDate = new Date().getTime() + (expiryDuration * 60 * 1000); // 60 = seconds, 1000 = miliseconds
    localStorage.setItem('expiryDate', expiryDate);
    localStorage.setItem('extended', false);
}
interval = setInterval(function() { // update the count down every 1 second
        var expiryDate = localStorage.expiryDate
            , now = new Date().getTime()
            , distance
            , hours, minutes, seconds;
        if (!expiryDate) return false;
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
            if (distance > 0 && distance <= 300000 && (localStorage.extended && localStorage.extended == 'false')) {
                if (!$('#timer-extension-modal').hasClass('show')) {
                    if (!$('body').hasClass('modal-open')) { // show when no other modal is opened
                        $('#timer-extension-modal').modal('show');
                    }
                }
            } else if (distance <= 0) {
                clearInterval(interval);
                localStorage.removeItem('expiryDate');
                localStorage.removeItem('extended');
                $('.modal').modal('hide');
                $('#timer-expired-modal').modal('show');
            }
        }
    }, 1000);


// timer extension
$('#form-timer-extension').submit(function() {
    event.preventDefault();
    var data = $(this).serializeArray();
    $.ajax({
        url: '/registration/timer_extension/',
        data: data,
        type: 'POST',
        success: function(result) {
            if ((result.status || 'error') == 'success') {
                if (result.registration_extended_expiry_duration) {
                    var initialExpiryDate = localStorage.expiryDate;
                    extendedExpiryDate = parseInt(initialExpiryDate) + (result.registration_extended_expiry_duration * 60 * 1000); // 60 = seconds, 1000 = miliseconds
                    localStorage.setItem('expiryDate', extendedExpiryDate);
                    localStorage.setItem('extended', true);
                    $('#timer-extension-modal').modal('hide');
                }
            } else {
                $('#timer-extension-modal').modal('hide');
                $('#timer-extension-modal').on('hidden.bs.modal', function(e) {
                    var errorMessage = (result.errors ? (result.errors.token_id ? result.errors.token_id[0] : gettext('Fail to extend timer')) : gettext('Fail to extend timer'));
                    modalAlert(gettext('Session Expiry Error'), errorMessage, gettext('OK'));
                    $('.modal:last').on('hidden.bs.modal', function(e) {
                        window.location.reload();
                    });
                });
            }
        }, error: function(xhr, text, error) {
            console.error('Error client: '+ error);
        }
    });
});


// timer expired
$('#timer-expired-modal').on('hidden.bs.modal', function (e) {
    window.location.href = '/pre_arrival/login/';
});


// progress bar
var currentProgressRate = JSON.parse($('#current-progress-rate').text() || '""');
$('.progress-page .progress-bar').css({
    'width': currentProgressRate +'%',
}).attr('aria-valuenow', currentProgressRate);
