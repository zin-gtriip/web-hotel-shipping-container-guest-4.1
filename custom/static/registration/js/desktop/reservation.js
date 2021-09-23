var reservationNo = JSON.parse($('#reservation').text() || '""');
var res_no = '';
gaTag('reservation_list_room', 'registration'); // google analytics


// event when reservation thumbnail is clicked
$('.reservation-container').click(function() {
    $(this).addClass('active')
        .find('input').prop('checked', true).change();
    $('.reservation-container:not(#'+ $(this).attr('id') +')').removeClass('active');
    res_no = $(this).find('input').val();
    gaTag('reservation_room_selected', 'registration'); // google analytics
});


// enable next button when one of reservation is selected
$('input[name=reservation_no]').change(function() {
    $('#btn-step-next').attr('disabled', false);
});


// default selected value condition
if (reservationNo == '') {
    $('.reservation-container:first').click();
} else {
    $('input[name=reservation_no][value='+ reservationNo +']').parents('.reservation-container').click();
}

var form = document.getElementById('reservation_form');
var isBookerRegistered = JSON.parse($('#isBookerRegistered').text() || '""');
var reservations = JSON.parse($('#reservations').text() || '""');
var skip_popup = false;

if(isBookerRegistered == false){
    $.each(reservations, function(index, r) {
        if(r.preArrivalDone == true && r.pmsNo == res_no){
            skip_popup = true;
        }
    });
}else{
    skip_popup = true;
}

if (skip_popup == false){
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        $('body').removeClass('loading');
	    var modal =
		    '<div class="modal fade" id="modal-confirmation" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true">' +
                '<div class="modal-dialog modal-dialog-centered modal-sm">'+
                    '<div class="modal-content">'+
                        '<div class="modal-header bg-primary text-white">'+
                            '<h4 class="modal-title mx-auto" id="modal-label-{{ forloop.counter0 }}">'+ gettext('Confirmation') +'</h4>'+
                        '</div>'+
                        '<div class="modal-body">'+ gettext('Will the guest who booked this reservation stay in this room?') +'</div>'+
                        '<div class="modal-footer justify-content-center">'+
                            '<button id="id-btn-no" type="button" class="btn btn-outline-primary" data-dismiss="modal">'+ gettext('No') +'</button>'+
                            '<button id="id-btn-yes" type="button" class="btn btn-primary">'+ gettext('Yes') +'</button>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
		    '</div>';
        $('.wrapper').append(modal);
        $('.modal:last').modal('show').addClass('shown');

        $('#id-btn-yes').click(function(){
            console.log("hello");
            console.log(document.getElementById('id_booker_stay'));
            document.getElementById('id_booker_stay').value = "yes";
            form.submit();
        });

        $('#id-btn-no').click(function(){
            document.getElementById('id_booker_stay').value = "no";
            form.submit();
        });
    });
}