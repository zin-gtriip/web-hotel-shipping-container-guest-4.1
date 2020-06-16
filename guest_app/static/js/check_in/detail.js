$('.datepicker').datepicker();

$(document).ready(function() {
    // fix input-prefix highlighted
    $('.input-prefix.active').removeClass('active');
});

$('#btn-add-extra').click(function() {
    var $extraTemplate = $('#extra-formset-template')
        , $newExtra = $extraTemplate.clone().removeAttr('hidden')
        , index = getFormsetIndex()
        , $newIsValid = $newExtra.find('#is-valid-template')
        , $newFirstName = $newExtra.find('#first-name-template')
        , $newLastName = $newExtra.find('#last-name-template')
        , $newNationality = $newExtra.find('#nationality-template')
        , $newPassportNo = $newExtra.find('#passport-no-template')
        , $newBirthDate = $newExtra.find('#birth-date-template')
        , $newBtnRemove = $newExtra.find('.btn-remove-extra');

    $newExtra.attr('id', 'extra-formset-'+ index).addClass('extra-formset');
    // is valid
    $newIsValid.attr('id', 'id_form-'+ index +'-is_valid').attr('name', 'form-'+ index +'-is_valid').val(true);
    // first name
    $newFirstName.siblings('label').attr('for', 'id_form-'+ index +'-first_name');
    $newFirstName.attr('id', 'id_form-'+ index +'-first_name').attr('name', 'form-'+ index +'-first_name');
    // last name
    $newLastName.siblings('label').attr('for', 'id_form-'+ index +'-last_name');
    $newLastName.attr('id', 'id_form-'+ index +'-last_name').attr('name', 'form-'+ index +'-last_name');
    // $newLastName.val('TEST');
    // nationality
    $newNationality.siblings('label').attr('for', 'id_form-'+ index +'-nationality');
    $newNationality.attr('id', 'id_form-'+ index +'-nationality').attr('name', 'form-'+ index +'-nationality').val('SG');
    // passport no
    $newPassportNo.siblings('label').attr('for', 'id_form-'+ index +'-passport_no');
    $newPassportNo.attr('id', 'id_form-'+ index +'-passport_no').attr('name', 'form-'+ index +'-passport_no');
    // birth date
    $newBirthDate.siblings('label').attr('for', 'id_form-'+ index +'-birth_date');
    $newBirthDate.attr('id', 'id_form-'+ index +'-birth_date').attr('name', 'form-'+ index +'-birth_date').datepicker();
    // remove button
    $newBtnRemove.click(function() {
        removeExtra($(this));
    });

    $newExtra.insertBefore($(this).closest('.row')); // insert before `.row` of `Add Guest` button 
    recalculateTotalExtra(); // `TOTAL_FORMS` needs to be updated
});

$('.btn-remove-extra').click(function() {
    removeExtra($(this));
});

function getFormsetIndex() {
    var $extraFormSet = $('.extra-formset');
    return $extraFormSet.length;
}

function recalculateTotalExtra() {
    var $extraFormSet = $('.extra-formset')
        , $totalFormset = $('#id_form-TOTAL_FORMS');
    $totalFormset.val($extraFormSet.length);
}

function rearrangeExtraIndex() {
    var index = 0;
    $('.extra-formset').each(function() {
        $(this).attr('id', 'extra-formset-'+ index);
        index++;
    });
}

function removeExtra($btn) {
    $btn.parents('.extra-formset').fadeOut(function() {
        $(this).remove();
        rearrangeExtraIndex();
        recalculateTotalExtra();
    });
}