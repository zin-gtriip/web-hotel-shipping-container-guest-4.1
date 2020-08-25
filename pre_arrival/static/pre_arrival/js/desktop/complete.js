$('#btn-ok').click(function() {
    var reservationNo = JSON.parse($('#reservation-no').text() || '""'); // set time we're counting down to
    try { reservationNo.postMessage(reservationNo); } catch(error) {} // send message to app
});
