$('#btn-ok').click(function() {
    var number = JSON.parse($('#reservation-no').text() || '""'); // set time we're counting down to
    try { reservationNo.postMessage(number); } catch(error) {} // send message to app
});
