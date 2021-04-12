window.addEventListener("flutterInAppWebViewPlatformReady", null); // add event to send message to app
gaTag('otherinfo_display', 'registration'); // google analytics


$('.new-window-link').click(function() {
    var app = JSON.parse($('#app').text() || '""');
    if (app) {
        try { window.flutter_inappwebview.callHandler('link', $(this).attr('href')); } catch(error) {} // send message to app
        return false;
    }
});


$('#btn-submit').click(function() {
    gaTag('otherinfo_submitted', 'registration'); // google analytics
});
