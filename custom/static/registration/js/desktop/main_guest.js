var mainGuest = JSON.parse($('#main_guest').text() || '""');
gaTag('reservation_list_guests', 'registration'); // google analytics

// event when reservation thumbnail is clicked
$('.main-guest-container').click(function() {
    $(this).find('input').prop('checked', true).change();
    gaTag('main_guest_selected', 'registration'); // google analytics

    var form = document.getElementById('main-guest-form');
    form.submit();
});