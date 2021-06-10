gaTag('guestlist_list_guests', 'registration'); // google analytics


$('#guests-list a').click(function() {
    if ($(this).data('is-main-guest') == '1') {
        gaTag('guestlist_select_main_guest', 'registration'); // google analytics
    } else {
        gaTag('guestlist_select_share_guest', 'registration'); // google analytics
    }
});


$('#btn-add').click(function() {
    gaTag('guestlist_add_guest', 'registration'); // google analytics
});
