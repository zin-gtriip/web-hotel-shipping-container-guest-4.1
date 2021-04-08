$('.datepicker').datepicker();


$('.btn-passport').click(function() {
    $('#id_is_submit').attr('checked', false);
});


$('#btn-back').click(function() {
	var modal =
		'<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true">' +
            '<div class="modal-dialog modal-dialog-centered modal-sm">'+
                '<div class="modal-content">'+
                    '<div class="modal-header bg-primary text-white">'+
                        '<h4 class="modal-title mx-auto" id="modal-label-{{ forloop.counter0 }}">'+ gettext('Warning') +'</h4>'+
                    '</div>'+
                    '<div class="modal-body">'+ gettext('All changes is not saved yet. Are you sure want to do this?') +'</div>'+
                    '<div class="modal-footer">'+
                        '<a href="/registration/guest_list/" class="btn btn-outline-primary mx-auto">'+ gettext('Yes') +'</a>'+
                        '<button type="button" class="btn btn-primary mx-auto" data-dismiss="modal">'+ gettext('No') +'</button>'+
                    '</div>'+
                '</div>'+
            '</div>'+
		'</div>';
    $('.wrapper').append(modal);
    $('.modal:last').modal('show').addClass('shown');
});
