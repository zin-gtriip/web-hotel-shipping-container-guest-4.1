// based on link below, we will use minimum canvas size to do validation
// https://github.com/jhildenbiddle/canvas-size
var maxCanvasWidth = 4096, maxCanvasHeight = 4096;
// accepted file type on uploading
var acceptedFileType = ['jpg', 'jpeg', 'png'];
// compressor options, for compressing captured and uploaded image
Compressor.setDefaults({
    mimeType: 'image/jpeg',
    quality: 0.6,
    maxWidth: maxCanvasWidth,
    maxHeight: maxCanvasHeight,
    convertSize: 2000000,
});
// croppie options, for scaling and rotating captured and uploaded image
// original calculation, calculate from `form-passport` width
// var scale = 1.33 // get from `640 / 480` desktop video size
//     , boundaryWidth = $('#form-passport').width()
//     , boundaryHeight = Math.floor(boundaryWidth / scale)
//     , viewportWidth = boundaryHeight
//     , viewportHeight = Math.floor(viewportWidth / scale);
var croppieOpts = {
    viewport: { width: 340, height: 240 },
    boundary: { width: screen.width, height: 525 },
    showZoomer: false,
    enableOrientation: true,
};


// btn-upload click
$('.file-capture, .file-upload').change(function() {
    var file = event.target.files[0];

    if (file === undefined) modalAlert(gettext('Invalid Image'), gettext('No image file selected'));
    if (!validateFileType($(this).val())) modalAlert(gettext('Invalid Image'), gettext('Please upload valid identification in JPEG/PNG format'));
    new Compressor(file, {
        success: function(result) {
            blobToDataURL(result, function(dataURL) {
                $('#img-preview').attr('src', dataURL);
                initCroppieComponents();
                initBorderGuide();
            });
        },
        error: function(err) {
            console.error('Compressor() error:'+ err.message);
            modalAlert(gettext('Error'), gettext('Error capturing image'));
        },
    });
});


// btn-next click
$('#btn-next').click(function() {
    var $img = $('#img-preview')
        , $passportFile = $('#id_passport_file');
        
    // disable all button
    $('.btn').attr('disabled', true).addClass('disabled');

    $img.croppie('result', {
        'type': 'blob',
        'size': 'original',
        'format': 'jpeg',
    }).then(function(blob) {
        blobToDataURL(blob, function(dataURL) {
            $passportFile.val(dataURL.substring(23)); // remove `data:image/jpeg;base64,` on dataURL
            $('#form-passport').submit();
        });
    });
});


// btn-skip click
$('#btn-skip').click(function() {
    $('#id_skip_passport').val(true);
    $('#form-passport').submit();
});


// validate file type
function validateFileType(fileName) {
    var splited = fileName.split('.')
        , fileType = (splited[splited.length - 1]).toLowerCase();
    if ((!fileName) || (splited.length <= 1) || (acceptedFileType.indexOf(fileType) < 0)) return false;
    return true;
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


// initiate croppie and additional elements
function initCroppieComponents() {
    var $timer = $('.timer-text').clone().removeClass('text-secondary').addClass('text-white')
        , $previewText = $('<div></div>').addClass('text-white text-center').attr('id', 'text-preview').text(gettext('Drag, rotate, or pinch the image to make sure that all information is within the box.'))
        , $iconRotate = $('<i></i>').addClass('fas fa-undo-alt').attr('aria-hidden', true)
        , $btnRotate = $('<button></button>').attr('type', 'button').addClass('btn btn-floating').attr('id', 'btn-rotate').data('degree', 90).html($iconRotate).click(function () {
            $('#img-preview').croppie('rotate', $(this).data('degree'));
        });

    $('.header, .page-header, .page-subheader, .default-container').hide();
    $('#img-preview').croppie('destroy').croppie(croppieOpts);
    $('.preview-container').show();
    $('.cr-boundary').append($timer, $previewText, $btnRotate);
}


// initiate border guide on croppie view port
function initBorderGuide() {
    var guideTopRight1 = $('<div></div>').addClass('guide-top-right-1')
        , guideTopRight2 = $('<div></div>').addClass('guide-top-right-2')
        , guideBottomRight1 = $('<div></div>').addClass('guide-bottom-right-1')
        , guideBottomRight2 = $('<div></div>').addClass('guide-bottom-right-2')
        , guideTopLeft1 = $('<div></div>').addClass('guide-top-left-1')
        , guideTopLeft2 = $('<div></div>').addClass('guide-top-left-2')
        , guideBottomLeft1 = $('<div></div>').addClass('guide-bottom-left-1')
        , guideBottomLeft2 = $('<div></div>').addClass('guide-bottom-left-2')

    $('.cr-boundary .cr-viewport').append(
        guideTopRight1,
        guideTopRight2,
        guideBottomRight1,
        guideBottomRight2,
        guideTopLeft1,
        guideTopLeft2,
        guideBottomLeft1,
        guideBottomLeft2
    );
}
