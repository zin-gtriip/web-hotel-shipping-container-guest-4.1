// submit language form 
$('#frm-set-language select#language').change(function() {
    $('#frm-set-language').submit();
});


// notification using bootstrap toast
$('.toast').toast('show');


// generate toast notify
function toastNotify(msg, bgColor='bg-danger', textColor='text-white') {
	var element = 
		'<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="10000">'+
			'<div class="toast-body '+ bgColor +'">'+
				'<span class="toast-message '+ textColor +'">'+ msg +'</span>'+
				'<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">'+
					'<span aria-hidden="true">&times;</span>'+
				'</button>'+
			'</div>'+
		'</div>';
	$('.toast-wrapper .toast-top-left').append(element);
    $('.toast').toast('show');
}
