// based on link below, we will use minimum canvas size to do validation
// https://github.com/jhildenbiddle/canvas-size
var maxCanvasWidth = 4096, maxCanvasHeight = 4096;
// accepted file type on uploading
var acceptedFileType = ['jpg', 'jpeg', 'png'];
// compressor options, for compressing captured and uploaded image
Compressor.setDefaults({
    mimeType: 'image/jpeg',
    quality: 1.0,
    maxWidth: maxCanvasWidth,
    maxHeight: maxCanvasHeight,
});
// form variable to be used in all code below
var $frmPassport = $('#frm-passport');
// croppie options, for scaling and rotating captured and uploaded image
// for desktop
var croppieOpts = {
    viewport: { width: 320, height: 240 },
    boundary: { width: 427, height: 320 },
    showZoomer: true,
    enableOrientation: true,
};
// for mobile
if (isMobile()) {
    // calculate from `frm-passport` width
    var scale = 1.33 // get from `640 / 480` desktop video size
        , boundaryWidth = $frmPassport.width()
        , boundaryHeight = Math.floor(boundaryWidth / scale)
        , viewportWidth = boundaryHeight
        , viewportHeight = Math.floor(boundaryHeight / scale);

    var croppieOpts = {
        viewport: { width: viewportWidth, height: viewportHeight },
        boundary: { width: boundaryWidth, height: boundaryHeight },
        showZoomer: true,
        enableOrientation: true,
    };
}


// document ready
$(document).ready(function () {
    if (isMobile()) {
        // mobile browser
        $('#vid-show, #btn-capture').attr('hidden', true);
        $('#btn-mobile-capture').attr('hidden', false);
    } else {
        // desktop browser
        // validate if any camera is available
        navigator.mediaDevices.getUserMedia({ video : true })
        .then(gotMedia)
        .catch(function(error) {
            console.error('getUserMedia() error:', error);
            toastNotify(gettext('No camera media is detected'));
        });
    }
});


// btn-rotate click
$('.btn-rotate').click(function() {
    $('#vid-img').croppie('rotate', $(this).data('degree'));
});


// btn-retake click
$('#btn-retake').click(function() {
    webCamera('on');
});


// btn-next click
$('#btn-next').click(function() {
    var $img = $('#vid-img')
        , $passportFile = $('#id_passport_file');

    $img.croppie('result', {
        'type': 'blob',
        'format': 'jpeg',
    }).then(function(blob) {
        blobToDataURL(blob, function(dataURL) {
            // remove `data:image/png;base64,` on dataURL
            $passportFile.val(dataURL.substring(23));
            $frmPassport.submit();
        });
    });
});


// btn-upload click
$('#file-upload, #file-mobile-capture').change(function(e) {
    var file = e.target.files[0]
        , $img = $('#vid-img');
    if (file === undefined) toastNotify(gettext('No image file selected'));
    if (!validateFileType($(this).val())) toastNotify(gettext('Please upload valid identification in JPEG/PNG format'));
    new Compressor(file, {
        success: function(result) {
            blobToDataURL(result, function(dataURL) {
                $img.attr('src', dataURL);
                webCamera('captured');
            });
        },
        error: function(err) {
            console.error('Compressor() error:'+ err.message);
            toastNotify(gettext('Error capturing image'));
        },
    });
});


// btn-skip click
$('#btn-skip').click(function() {
    $('#id_skip_passport').val(true);
    $frmPassport.submit();
});


// initiate camera, after validation
function gotMedia(stream) {
    var video = document.getElementById('vid-show')
        , $img = $('#vid-img')
        , $capture = $('#btn-capture');
    video.srcObject = stream;
    video.play();

    $capture.click(function() {
        var draw = document.createElement('canvas')
            , context2D = draw.getContext('2d');
        draw.width = video.videoWidth;
        draw.height = video.videoHeight;
        context2D.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
        new Compressor(dataURLtoBlob(draw.toDataURL('image/jpeg')), {
            success: function(result) {
                blobToDataURL(result, function(dataURL) {
                    $img.attr('src', dataURL);
                    webCamera('captured');
                });
            },
            error: function(err) {
                console.error('Compressor() error:'+ err.message);
                toastNotify(gettext('Error capturing image'));
            },
        });
    });
}


// blob to dataURL
function blobToDataURL(blob, callback) {
    var reader = new FileReader();
    reader.onload = function(e) { callback(e.target.result); }
    reader.readAsDataURL(blob);
}


// dataURL to blob
function dataURLtoBlob(dataURL) {
    var arr = dataURL.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}


// switch video
function webCamera(state) {
    var video = document.getElementById('vid-show');

    if (state == 'on') {
        $('#vid-img').croppie('destroy');
        $('#btn-upload').attr('hidden', false);
        $('#vid-img, #btn-next, #btn-retake').attr('hidden', true);
        if (isMobile()) {
            $('#btn-mobile-capture').attr('hidden', false).click();
        } else {
            video.play();
            $(video).attr('hidden', false);
            $('#btn-capture').attr('hidden', false);
        }
    } else if (state == 'captured') {
        if (isMobile()) {
            $('#btn-mobile-capture').attr('hidden', true);
        } else {
            video.pause();
            $(video).attr('hidden', true);
            $('#btn-capture').attr('hidden', true);
        }
        $('#vid-img').attr('hidden', false).croppie(croppieOpts);
        $('#btn-upload').attr('hidden', true);
        $('#btn-next, #btn-retake').attr('hidden', false);
        // add rotate buttons
        $('.cr-slider-wrap').prepend(
            '<button type="button" class="btn btn-link waves-effect text-primary px-3 btn-rotate" data-degree="90">'+
                '<i class="fas fa-undo-alt" aria-hidden="true"></i>'+
            '</button>'
        ).append(
            '<button type="button" class="btn btn-link waves-effect text-primary px-3 btn-rotate" data-degree="-90">'+
                '<i class="fas fa-redo-alt" aria-hidden="true"></i>'+
            '</button>'
        );
        // add click event to rotate buttons
        $('.btn-rotate').click(function () {
            $('#vid-img').croppie('rotate', $(this).data('degree'));
        });
    }
}


// validate file type
function validateFileType(fileName) {
    var splited = fileName.split('.')
        , fileType = (splited[splited.length - 1]).toLowerCase();
    if ((!fileName) || (splited.length <= 1) || (acceptedFileType.indexOf(fileType) < 0)) return false;
    return true;
}


// validate if it is mobile
function isMobile() {
    var toMatch = [
        /Android/i,
        /webOS/i,
        /iPhone/i,
        /iPad/i,
        /iPod/i,
        /BlackBerry/i,
        /Windows Phone/i
    ];

    return toMatch.some((toMatchItem) => {
        return navigator.userAgent.match(toMatchItem);
    });
}