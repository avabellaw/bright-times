$('#edit-btn').click(function() {
    isEditing = $(this).attr('data-editing') === 'true';
    isEditing = !isEditing;
    $(this).attr('data-editing', isEditing);

    window.location.hash = '#detail-form';

    $('.editable-field').prop('disabled', !isEditing).prop('readonly', !isEditing)

    $('#save-btn').toggleClass('d-none');
    $('#edit-btn').toggleClass('d-none');
    $('#cancel-btn').toggleClass('d-none');
});