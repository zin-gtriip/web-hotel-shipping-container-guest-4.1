$('.datepicker').datepicker();
gaTag('detail_guest_display', 'registration'); // google analytics


var gaOcrSuccess = JSON.parse($('#ga-ocr-success').text() || '""');
if (gaOcrSuccess) {
    gaTag('ocr_guest_success', 'registration'); // google analytics
}


$('.btn-ocr').click(function() {
    $('#id_is_submit').attr('checked', false);
});


$('#btn-back').click(function() {
	var modal =
		'<div class="modal fade" id="modal-confirmation" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true">' +
            '<div class="modal-dialog modal-dialog-centered modal-sm">'+
                '<div class="modal-content">'+
                    '<div class="modal-header bg-primary text-white">'+
                        '<h4 class="modal-title mx-auto" id="modal-label-{{ forloop.counter0 }}">'+ gettext('Warning') +'</h4>'+
                    '</div>'+
                    '<div class="modal-body">'+ gettext('All changes is not saved yet. Are you sure want to do this?') +'</div>'+
                    '<div class="modal-footer justify-content-center">'+
                        '<a href="/registration/guest_list/" class="btn btn-outline-primary">'+ gettext('Yes') +'</a>'+
                        '<button type="button" class="btn btn-primary" data-dismiss="modal">'+ gettext('No') +'</button>'+
                    '</div>'+
                '</div>'+
            '</div>'+
		'</div>';
    $('.wrapper').append(modal);
    $('.modal:last').modal('show').addClass('shown');
});


$('#btn-save').click(function() {
    var isMainGuest = JSON.parse($('#is-main-guest').text() || '""');
    if (isMainGuest) {
        gaTag('detail_mainguest_submitted', 'registration'); // google analytics
    } else {
        gaTag('detail_sharerguest_submitted', 'registration'); // google analytics
    }
});
