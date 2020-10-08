window.addEventListener("flutterInAppWebViewPlatformReady", null); // add event to send message to app


$('#btn-ok').click(function() {
    var number = JSON.parse($('#reservation-no').text() || '""');
    try { window.flutter_inappwebview.callHandler('reservationNo', number); } catch(error) {} // send message to app
});

$('#phone-store').click(function(){
    if(navigator.userAgent.toLowerCase().indexOf("android") > -1){
        window.location.href = 'http://play.google.com/store/apps';
    }
    if(navigator.userAgent.toLowerCase().indexOf("iphone") > -1){
        window.location.href = 'http://itunes.apple.com';
    }
});