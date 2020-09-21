$('.datepicker').datepicker();
restyleExtra();
rearrangeExtraIndex();
validateMaxExtra();


$(document).ready(function() {
    $('.input-prefix.active').removeClass('active'); // fix input-prefix highlighted
});


$('#btn-add-extra').click(function() {
    var $extraTemplate = $('#extra-formset-template')
        , $newExtra = $extraTemplate.clone().removeAttr('hidden').addClass('extra-formset')
        , index = getFormsetIndex()
        , $newGuestId = $newExtra.find('#guest-id-template')
        , $newFirstName = $newExtra.find('#first-name-template')
        , $newLastName = $newExtra.find('#last-name-template')
        , $newNationality = $newExtra.find('#nationality-template')
        , $newPassportNo = $newExtra.find('#passport-no-template')
        , $newBirthDate = $newExtra.find('#birth-date-template')
        , $newBtnRemove = $newExtra.find('.btn-remove-extra');

    // guest id
    $newGuestId.attr('id', 'id_form-'+ index +'-guest_id').attr('name', 'form-'+ index +'-guest_id');
    // first name
    $newFirstName.siblings('label').attr('for', 'id_form-'+ index +'-first_name');
    $newFirstName.attr('id', 'id_form-'+ index +'-first_name').attr('name', 'form-'+ index +'-first_name').attr('required', true);
    // last name
    $newLastName.siblings('label').attr('for', 'id_form-'+ index +'-last_name');
    $newLastName.attr('id', 'id_form-'+ index +'-last_name').attr('name', 'form-'+ index +'-last_name').attr('required', true);
    // $newLastName.val('TEST');
    // nationality
    $newNationality.siblings('label').attr('for', 'id_form-'+ index +'-nationality');
    $newNationality.attr('id', 'id_form-'+ index +'-nationality').attr('name', 'form-'+ index +'-nationality').attr('required', true).val('SG');
    // passport no
    $newPassportNo.siblings('label').attr('for', 'id_form-'+ index +'-passport_no');
    $newPassportNo.attr('id', 'id_form-'+ index +'-passport_no').attr('name', 'form-'+ index +'-passport_no').attr('required', true);
    // birth date
    $newBirthDate.siblings('label').attr('for', 'id_form-'+ index +'-birth_date');
    $newBirthDate.attr('id', 'id_form-'+ index +'-birth_date').attr('name', 'form-'+ index +'-birth_date').datepicker();
    // remove button
    $newBtnRemove.click(function() {
        removeExtra($(this));
    });

    $newExtra.appendTo($('.guests'));
    restyleExtra();
    rearrangeExtraIndex();
    recalculateTotalExtra(); // `TOTAL_FORMS` needs to be updated
    validateMaxExtra(); // disable `btn-add-extra` if max is reached
});


$('.btn-remove-extra').click(function() {
    removeExtra($(this));
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
