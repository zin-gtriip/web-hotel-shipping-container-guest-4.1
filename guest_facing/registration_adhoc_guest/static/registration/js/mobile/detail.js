$('.datepicker').datepicker();
$('.rolldate').each(function() {
    initRolldate($(this));
});
restyleExtra();
rearrangeExtraIndex();
validateMaxExtra();
scrollToGuestIndex();
showHideBackBtn();
validateRedirect();


$(document).ready(function() {
    $('.input-prefix.active').removeClass('active'); // fix input-prefix highlighted
});


$('#btn-add-extra').click(function() {
    $('#form-type').val('add_guest');
});


$('#btn-skip, #btn-next').click(function() {
    $('#form-type').val('submit');
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
        $(this).find('[name^=form-]').each(function() { // change `name`, `id` for every input
            var elementName = $(this).attr('name')
                , elementId = $(this).attr('id');
            elementName = elementName.replace(/form-\d+/g, 'form-'+index);
            elementId = elementId.replace(/id_form-\d+/g, 'id_form-'+index);
            $(this).attr('name', elementName).attr('id', elementId);
        });
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
        scrollToGuestIndex();
        showHideBackBtn();
        validateRedirect();
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
    var $extraFormset = $('.extra-formset:visible');

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
        , $btnAddExtra = $('#btn-add-extra')
        , $btnSkip = $('#btn-skip')
        , $btnNext = $('#btn-next');
    
    if ($extraFormset.length >= $maxFormset.val()) {
        $btnAddExtra.hide();
        $btnSkip.hide();
        $btnNext.show();
    } else {
        $btnAddExtra.show();
        $btnSkip.show();
        $btnNext.hide();
    }
}


function scrollToGuestIndex() {
    $('html, body').animate({
        scrollTop: $('.guest-index:last').offset().top
    }, 800);
}


function showHideBackBtn() {
    if ($('.extra-formset:visible').length == 0) {
        $('#btn-back').show();
    } else {
        $('#btn-back').hide();
    }
}


function validateRedirect() {
    if (!$('#main-guest').is(':visible') && $('.extra-formset:visible').length == 0) {
        window.location.href = '/pre_arrival/guest_list/';
    }
}
