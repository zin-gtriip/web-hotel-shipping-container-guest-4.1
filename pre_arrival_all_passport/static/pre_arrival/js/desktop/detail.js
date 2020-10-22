$('.datepicker').datepicker();
restyleExtra();
rearrangeExtraIndex();
validateMaxExtra();


$(document).ready(function() {
    $('.input-prefix.active').removeClass('active'); // fix input-prefix highlighted
});


$('#btn-add-extra').click(function() {
    $('#form-type').val('add_guest').parents('form').submit();
});


$('.btn-remove-extra').click(function() {
    removeExtra($(this));
});


$('.modal').on('hide.bs.modal', function() {
    var guestID = $(this).find('#guest-id').val();
    if (guestID !== undefined) {
        window.location.href = '/pre_arrival/extra_passport/?guest_id='+ guestID;
    }
});


function getFormsetIndex() {
    return $('.extra-formset').length;
}


function recalculateTotalExtra() {
    var $extraFormSet = $('.extra-formset')
        , $totalFormset = $('#id_form-TOTAL_FORMS');
    $totalFormset.val($extraFormSet.length);
}


function rearrangeExtraIndex() {
    var $extraFormset = $('.extra-formset')
        , $mainGuest = $('#main-guest');

    $extraFormset.each(function(index) {
        $(this).attr('id', 'extra-formset-'+ index)
            .find('.guest-index span').text(gettext('Guest') +' '+ (index + 2)); // extra formset starts from 2
    });

    // add or remove main guest title
    if ($extraFormset.length > 0) {
        $mainGuest.find('.guest-index span').text(gettext('Main Guest'));
    } else {
        $mainGuest.find('.guest-index span').text('');
    }
}


function removeExtra($btn) {
    $btn.parents('.extra-formset').fadeOut(function() {
        $(this).remove();
        restyleExtra();
        rearrangeExtraIndex();
        recalculateTotalExtra();
        validateMaxExtra();
    });
}


function restyleExtra() {
    var $extraFormset = $('.extra-formset')
        , $mainGuest = $('#main-guest');

    $extraFormset.each(function(index) {
        $(this).removeClass('even');
        if (index % 2 == 0) {
            $(this).addClass('even');
        }
    });

    if ($extraFormset.length <= 0) {
        $mainGuest.removeClass('ml-auto').addClass('mx-auto');
    } else if ($extraFormset.length == 1) {
        $mainGuest.removeClass('mx-auto').addClass('ml-auto');
    } else {
        $mainGuest.removeClass('ml-auto, mx-auto');
    }
    $('.guests > div:not(#main-guest, #extra-formset-template, :last-child)').removeClass('mr-auto');
}


function validateMaxExtra() {
    var $extraFormset = $('.extra-formset')
        , $maxFormset = $('#id_form-MAX_NUM_FORMS')
        , $btnAddExtra = $('#btn-add-extra');
    
    if ($extraFormset.length >= $maxFormset.val()) {
        $btnAddExtra.attr('disabled', true);
    } else {
        $btnAddExtra.removeAttr('disabled');
    }
}
