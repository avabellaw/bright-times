$('#edit-btn').click(function() {
    is_editing = $(this).attr('data-editing') === 'true';
    is_editing = !is_editing;
    $(this).attr('data-editing', is_editing);

    window.location.hash = '#detail-form';

    $('input').prop('disabled', !is_editing);
    $('input').prop('readonly', !is_editing);

    $('#save-btn').toggleClass('d-none');
    $('#edit-btn').toggleClass('d-none');
    $('#cancel-btn').toggleClass('d-none');
});