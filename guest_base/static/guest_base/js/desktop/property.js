// event when reservation thumbnail is clicked
$('.property-container').click(function() {
    $(this).find('input').prop('checked', true).change();
    $('#form-property').submit();
});
