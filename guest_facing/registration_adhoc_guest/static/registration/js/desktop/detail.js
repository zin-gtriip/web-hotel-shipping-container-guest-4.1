$('.datepicker').datepicker();
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


function restyleExtra() {
    var $extraFormset = $('.extra-formset:visible')
        , $mainGuest = $('#main-guest');

    $extraFormset.each(function(index) {
        $(this).removeClass('even');
        if (index % 2 == 0) {
            $(this).addClass('even');
        }
    });

    if ($mainGuest.is(':visible')) {
        if ($extraFormset.length <= 0) {
            $mainGuest.removeClass('ml-auto').addClass('mx-auto');
        } else if ($extraFormset.length == 1) {
            $mainGuest.removeClass('mx-auto').addClass('ml-auto');
            $extraFormset.addClass('mr-auto');
        } else {
            $mainGuest.removeClass('ml-auto, mx-auto');
        }
    } else {
        if ($extraFormset.length == 1) {
            $extraFormset.addClass('mx-auto');
        } else if ($extraFormset.length == 2) {
            $extraFormset.first().addClass('ml-auto');
        }
    }
    $('.guests > div:not(#main-guest, #extra-formset-template, :last-child)').removeClass('mr-auto');
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
        window.location.href = '/registration/guest_list/';
    }
}
