$('.datepicker').datepicker();
$('.rolldate').each(function() {
    initRolldate($(this));
});
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


function initRolldate($rolldate) {
    var rollDate
        , $datepicker = $rolldate.parents('.md-form').find('.datepicker');

    $rolldate.removeAttr('required');
    rollDate = new Rolldate({
        el: '#'+ $rolldate.attr('id'),
        format: 'YYYY-MM-DD',
        beginYear: 1900,
        endYear: new Date().getFullYear(),
        value: $rolldate.val(),
        lang: {
            title: gettext('Select Date'),
            cancel: gettext('Cancel'),
            confirm: gettext('Confirm'),
            year: '', month: '', day: '', hour: '', min: '', sec: ''},
        confirm: function(date) {
            $datepicker.datepicker('update', new Date(date));
        },
    });
    $datepicker.datepicker('update', new Date($rolldate.val()));
    $datepicker.click(function() {
        rollDate.show();
    });
    $datepicker.focus(function() {
        rollDate.show();
    });
}


function restyleExtra() {
    var $extraFormset = $('.extra-formset');

    $extraFormset.each(function(index) {
        $(this).removeClass('even');
        if (index % 2 == 0) {
            $(this).addClass('even');
        }
    });
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
