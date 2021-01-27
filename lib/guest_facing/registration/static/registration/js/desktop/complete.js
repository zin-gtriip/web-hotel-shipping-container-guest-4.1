window.addEventListener("flutterInAppWebViewPlatformReady", null); // add event to send message to app


$('#btn-ok').click(function() {
    var number = JSON.parse($('#reservation-no').text() || '""');
    try { window.flutter_inappwebview.callHandler('reservationNo', number); } catch(error) {} // send message to app
});
