$("#edit-btn").click(function() {
    let isEditing = $(this).attr("data-editing") === "true";
    isEditing = !isEditing;
    $(this).attr("data-editing", isEditing);

    window.location.hash = "#detail-form";

    $(".editable-field:not([type='file'])").prop("disabled", !isEditing).prop(
        "readonly", !isEditing);
    $(".editable-field[type='file']").prop("disabled", !isEditing);

    $("#save-btn").toggleClass("d-none");
    $("#edit-btn").toggleClass("d-none");
    $("#cancel-btn").toggleClass("d-none");
});