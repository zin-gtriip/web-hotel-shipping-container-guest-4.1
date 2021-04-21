gaTag('list_property', 'property'); // google analytics


// event when reservation thumbnail is clicked
$('.property-container').click(function() {
    $(this).find('input').prop('checked', true).change();
    gaTag('property_selected', 'registration'); // google analytics
    $('#form-property').submit();
});
