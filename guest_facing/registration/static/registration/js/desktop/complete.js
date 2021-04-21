window.addEventListener("flutterInAppWebViewPlatformReady", null); // add event to send message to app
gaTag('complete_display', 'registration'); // google analytics


$('#btn-ok').click(function() {
    var number = JSON.parse($('#reservation-no').text() || '""');
    try { window.flutter_inappwebview.callHandler('reservationNo', number); } catch(error) {} // send message to app
});


$('#btn-next-registration').click(function() {
    gaTag('complete_next_registration', 'registration'); // google analytics
});


$('.anchor-app-store').click(function() {
    gaTag('complete_app_store', 'registration'); // google analytics
});


$('.anchor-play-store').click(function() {
    gaTag('complete_play_store', 'registration'); // google analytics
});


$('.anchor-general-download').click(function() {
    gaTag('complete_general_download', 'registration'); // google analytics
});
